import tkinter as tk


class PullBulbApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Pull Cord Bulb Toggle")
        self.root.geometry("460x620")
        self.root.resizable(False, False)

        # Warm beige/tan background matching the reference screen
        self.bg_color = "#DFCF9B"
        self.canvas = tk.Canvas(
            root,
            width=460,
            height=620,
            bg=self.bg_color,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Center and geometry configuration
        self.cx = 230
        self.bulb_center_y = 215
        self.socket_top_y = 282
        self.socket_bottom_y = 325
        self.cord_top_y = 325

        # Cord pull physics state
        self.base_cord_length = 125
        self.cord_length = float(self.base_cord_length)
        self.max_pull_length = 225
        self.pull_threshold = 165  # Drag past this Y to toggle ON/OFF

        self.is_on = False
        self.dragging = False
        self.drag_start_y = 0
        self.drag_start_len = float(self.base_cord_length)
        self.toggled_this_drag = False
        self.spring_job = None

        self._draw_scene()
        self._bind_events()

    def _draw_scene(self) -> None:
        self.canvas.delete("all")

        # Status label at top
        status_text = "BULB: ON  (Drag cord down to turn OFF)" if self.is_on else "BULB: OFF (Drag cord down to turn ON)"
        self.canvas.create_text(
            self.cx,
            45,
            text=status_text,
            fill="#3B3522",
            font=("Segoe UI", 12, "bold"),
            tags="ui",
        )

        cord_bottom_y = self.cord_top_y + self.cord_length

        # Soft outer glow when bulb is ON
        if self.is_on:
            glow_radii = [115, 92, 72]
            glow_colors = ["#EAE0A8", "#F2E7A7", "#FAF0AA"]
            for r, col in zip(glow_radii, glow_colors):
                self.canvas.create_oval(
                    self.cx - r,
                    self.bulb_center_y - r,
                    self.cx + r,
                    self.bulb_center_y + r,
                    fill=col,
                    outline="",
                    tags="bulb",
                )

        # Pull wire / cord
        self.canvas.create_line(
            self.cx,
            self.cord_top_y,
            self.cx,
            cord_bottom_y,
            fill="#2B271D",
            width=4,
            capstyle="round",
            tags=("cord", "draggable"),
        )

        # Pull knob at the end of the cord
        knob_r = 9
        self.canvas.create_oval(
            self.cx - knob_r,
            cord_bottom_y - knob_r,
            self.cx + knob_r,
            cord_bottom_y + knob_r,
            fill="#4A4435",
            outline="#2B271D",
            width=3,
            tags=("cord", "draggable"),
        )

        # Bulb glass body (top rounded dome + tapered neck)
        glass_fill = "#FFF475" if self.is_on else "#DCE3A1"
        r = 64

        # Dome oval
        self.canvas.create_oval(
            self.cx - r,
            self.bulb_center_y - r,
            self.cx + r,
            self.bulb_center_y + r,
            fill=glass_fill,
            outline="#2B271D",
            width=4,
            tags="bulb",
        )

        # Tapered lower glass connecting to socket
        neck_poly = [
            self.cx - 48, self.bulb_center_y + 40,
            self.cx + 48, self.bulb_center_y + 40,
            self.cx + 30, self.socket_top_y + 4,
            self.cx - 30, self.socket_top_y + 4,
        ]
        self.canvas.create_polygon(
            neck_poly,
            fill=glass_fill,
            outline="#2B271D",
            width=4,
            joinstyle="round",
            tags="bulb",
        )

        # Cover inner seam line between dome and tapered neck for clean outline
        self.canvas.create_arc(
            self.cx - r + 2,
            self.bulb_center_y - r + 2,
            self.cx + r - 2,
            self.bulb_center_y + r - 2,
            start=212,
            extent=116,
            style="arc",
            outline=glass_fill,
            width=5,
            tags="bulb",
        )

       # Subtle highlight reflection on bulb glass
        highlight_color = "#FFFDF0" if self.is_on else "#EFF4C8"
        self.canvas.create_arc(
            self.cx - 44,
            self.bulb_center_y - 44,
            self.cx + 44,
            self.bulb_center_y + 44,
            start=110,
            extent=55,
            style="arc",
            outline=highlight_color,
            width=5,
            tags="bulb",
        )

        # Filament inside bulb
        filament_color = "#FF9800" if self.is_on else "#7A7662"
        self.canvas.create_line(
            self.cx - 14,
            self.socket_top_y + 2,
            self.cx - 14,
            self.bulb_center_y + 18,
            fill=filament_color,
            width=3,
            tags="bulb",
        )
        self.canvas.create_line(
            self.cx + 14,
            self.socket_top_y + 2,
            self.cx + 14,
            self.bulb_center_y + 18,
            fill=filament_color,
            width=3,
            tags="bulb",
        )
        self.canvas.create_arc(
            self.cx - 16,
            self.bulb_center_y + 6,
            self.cx + 16,
            self.bulb_center_y + 28,
            start=0,
            extent=180,
            style="arc",
            outline=filament_color,
            width=3,
            tags="bulb",
        )

        # Metallic screw base / socket
        self.canvas.create_rectangle(
            self.cx - 31,
            self.socket_top_y,
            self.cx + 31,
            self.socket_bottom_y,
            fill="#9E9E9E",
            outline="#2B271D",
            width=4,
            tags="socket",
        )

        # Screw thread lines
        for y_line in (self.socket_top_y + 14, self.socket_top_y + 28):
            self.canvas.create_line(
                self.cx - 29,
                y_line,
                self.cx + 29,
                y_line,
                fill="#2B271D",
                width=3,
                tags="socket",
            )

        # Bottom instruction
        self.canvas.create_text(
            self.cx,
            575,
            text="Wire ko mouse se pakad kar neeche drag karein",
            fill="#4E4732",
            font=("Segoe UI", 10),
            tags="ui",
        )

    def _bind_events(self) -> None:
        self.canvas.tag_bind("draggable", "<Enter>", self._on_enter)
        self.canvas.tag_bind("draggable", "<Leave>", self._on_leave)
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _event: tk.Event) -> None:
        self.canvas.config(cursor="hand2")

    def _on_leave(self, _event: tk.Event) -> None:
        if not self.dragging:
            self.canvas.config(cursor="")

    def _on_press(self, event: tk.Event) -> None:
        if self.spring_job is not None:
            self.root.after_cancel(self.spring_job)
            self.spring_job = None

        self.dragging = True
        self.drag_start_y = event.y
        self.drag_start_len = self.cord_length
        self.toggled_this_drag = False
        self.canvas.config(cursor="fleur")

    def _on_drag(self, event: tk.Event) -> None:
        if not self.dragging:
            return

        delta_y = event.y - self.drag_start_y
        new_len = self.drag_start_len + delta_y
        self.cord_length = max(
            float(self.base_cord_length),
            min(float(self.max_pull_length), new_len),
        )

        # Toggle once when pulled down past threshold
        if not self.toggled_this_drag and self.cord_length >= self.pull_threshold:
            self.is_on = not self.is_on
            self.toggled_this_drag = True

        self._draw_scene()

    def _on_release(self, _event: tk.Event) -> None:
        if not self.dragging:
            return

        self.dragging = False
        self.canvas.config(cursor="")
        self._animate_spring_back()

    def _animate_spring_back(self) -> None:
        diff = self.cord_length - self.base_cord_length
        if abs(diff) < 1.0:
            self.cord_length = float(self.base_cord_length)
            self._draw_scene()
            self.spring_job = None
            return

        # Smooth spring return toward original length
        self.cord_length -= diff * 0.28
        self._draw_scene()
        self.spring_job = self.root.after(16, self._animate_spring_back)


if __name__ == "__main__":
    app_root = tk.Tk()
    PullBulbApp(app_root)
    app_root.mainloop()