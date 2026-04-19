import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# ──────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────
BRUSH_THICKNESS = 5
ERASER_THICKNESS = 50
SMOOTHING = 4          # deque length for smoothing lines

COLORS = {
    "Blue":   (255, 0, 0),
    "Green":  (0, 255, 0),
    "Red":    (0, 0, 255),
    "Yellow": (0, 255, 255),
}

# UI Layout
TOOLBAR_HEIGHT = 70
COLOR_BTN_W = 120
ERASER_BTN_W = 120
CLEAR_BTN_W = 100

# ──────────────────────────────────────────
# STATE
# ──────────────────────────────────────────
selected_color = "Blue"
draw_color = COLORS[selected_color]
drawing_mode = "draw"   # "draw" | "erase"

# Smoothed point buffers (one per color + eraser)
points = {name: deque(maxlen=SMOOTHING) for name in COLORS}
points["Eraser"] = deque(maxlen=SMOOTHING)

# Full stroke history for re-drawing
strokes = []            # list of {"color": BGR, "pts": [(x,y),...], "thickness": int}
current_stroke = None

# ──────────────────────────────────────────
# MEDIAPIPE SETUP
# ──────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
)

# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────
def fingers_up(lm, w, h):
    """Return [index_up, middle_up] as booleans."""
    tips = [8, 12]   # index tip, middle tip
    pips = [6, 10]   # index pip, middle pip
    up = []
    for tip, pip in zip(tips, pips):
        up.append(lm[tip].y < lm[pip].y)
    return up

def get_landmark_px(lm, idx, w, h):
    return int(lm[idx].x * w), int(lm[idx].y * h)

def build_toolbar(w):
    """Draw the top toolbar onto a blank image."""
    bar = np.zeros((TOOLBAR_HEIGHT, w, 3), dtype=np.uint8)
    bar[:] = (30, 30, 30)

    x = 10
    for name, bgr in COLORS.items():
        cv2.rectangle(bar, (x, 10), (x + COLOR_BTN_W - 10, TOOLBAR_HEIGHT - 10), bgr, -1)
        label = name
        if selected_color == name and drawing_mode == "draw":
            cv2.rectangle(bar, (x, 10), (x + COLOR_BTN_W - 10, TOOLBAR_HEIGHT - 10), (255,255,255), 3)
        cv2.putText(bar, label, (x + 8, TOOLBAR_HEIGHT - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
        x += COLOR_BTN_W

    # Eraser button
    eraser_x = x
    ec = (180, 180, 180)
    cv2.rectangle(bar, (eraser_x, 10), (eraser_x + ERASER_BTN_W - 10, TOOLBAR_HEIGHT - 10), ec, -1)
    if drawing_mode == "erase":
        cv2.rectangle(bar, (eraser_x, 10), (eraser_x + ERASER_BTN_W - 10, TOOLBAR_HEIGHT - 10), (255,255,255), 3)
    cv2.putText(bar, "Eraser", (eraser_x + 10, TOOLBAR_HEIGHT - 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    x += ERASER_BTN_W

    # Clear button
    clear_x = x
    cv2.rectangle(bar, (clear_x, 10), (clear_x + CLEAR_BTN_W - 10, TOOLBAR_HEIGHT - 10), (50,50,200), -1)
    cv2.putText(bar, "Clear", (clear_x + 12, TOOLBAR_HEIGHT - 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    return bar, eraser_x, clear_x

def toolbar_click(mx, my, eraser_x, clear_x):
    """Returns ('color', name) | ('erase',) | ('clear',) | None"""
    global selected_color, drawing_mode, draw_color
    if my > TOOLBAR_HEIGHT:
        return None
    x = 10
    for name in COLORS:
        if x <= mx <= x + COLOR_BTN_W - 10:
            selected_color = name
            drawing_mode = "draw"
            draw_color = COLORS[name]
            return ("color", name)
        x += COLOR_BTN_W
    if eraser_x <= mx <= eraser_x + ERASER_BTN_W - 10:
        drawing_mode = "erase"
        return ("erase",)
    if clear_x <= mx <= clear_x + CLEAR_BTN_W - 10:
        return ("clear",)
    return None

# ──────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

canvas = None   # initialized on first frame

print("Air Canvas running — press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)          # mirror
    h, w = frame.shape[:2]

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # ── Hand detection ──────────────────────
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    ix, iy = -1, -1   # index fingertip position

    if result.multi_hand_landmarks:
        for hand_lm in result.multi_hand_landmarks:
            lm = hand_lm.landmark
            mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

            idx_up, mid_up = fingers_up(lm, w, h)
            ix, iy = get_landmark_px(lm, 8, w, h)

            # ── Selection mode (2 fingers up) ────
            if idx_up and mid_up:
                current_stroke = None   # stop drawing
                # Detect toolbar click via gesture
                if iy < TOOLBAR_HEIGHT:
                    bar, eraser_x, clear_x = build_toolbar(w)
                    action = toolbar_click(ix, iy, eraser_x, clear_x)
                    if action and action[0] == "clear":
                        canvas = np.zeros((h, w, 3), dtype=np.uint8)
                        strokes.clear()
                # Draw a circle to show hover position
                cv2.circle(frame, (ix, iy), 12, (0, 255, 0), 2)

            # ── Drawing mode (1 finger up) ───────
            elif idx_up and not mid_up and iy > TOOLBAR_HEIGHT:
                if current_stroke is None:
                    thickness = ERASER_THICKNESS if drawing_mode == "erase" else BRUSH_THICKNESS
                    color = (0, 0, 0) if drawing_mode == "erase" else draw_color
                    current_stroke = {"color": color, "pts": [], "thickness": thickness}
                    strokes.append(current_stroke)

                current_stroke["pts"].append((ix, iy))

                # Draw the latest segment live on canvas
                pts = current_stroke["pts"]
                if len(pts) >= 2:
                    cv2.line(canvas, pts[-2], pts[-1],
                             current_stroke["color"],
                             current_stroke["thickness"])

                cv2.circle(frame, (ix, iy), 8,
                           (0,0,0) if drawing_mode=="erase" else draw_color, -1)
            else:
                current_stroke = None

    # ── Merge canvas onto frame ──────────────
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(canvas_gray, 5, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    merged = cv2.add(frame_bg, canvas_fg)

    # ── Draw toolbar ─────────────────────────
    bar, eraser_x, clear_x = build_toolbar(w)
    merged[:TOOLBAR_HEIGHT] = bar

    # Cursor indicator in toolbar area
    if 0 < ix < w and 0 < iy < TOOLBAR_HEIGHT:
        cv2.circle(merged, (ix, iy), 10, (255, 255, 255), 2)

    # ── HUD ──────────────────────────────────
    mode_label = f"Mode: {'ERASER' if drawing_mode=='erase' else selected_color}"
    cv2.putText(merged, mode_label, (10, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                (200,200,200), 2)
    cv2.putText(merged, "1 finger = Draw  |  2 fingers = Select/Hover  |  Q = Quit",
                (w//2 - 280, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 1)

    cv2.imshow("Air Canvas", merged)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()