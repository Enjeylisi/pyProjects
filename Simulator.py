
import tkinter as tk
from tkinter import ttk
import random
import calendar
import math

class FactoryGame:
    def __init__(self, root, sector):
        self.root = root
        self.sector = sector
        self.year = 2027
        self.month = 1
        self.day = 1
        self.money = 50000
        self.workers = 5
        self.security = 2
        self.speed = 1
        self.contract = None
        self.contract_days = 0
        self.month_income = 0
        self.month_expenses = 0
        self.total_income = 0
        self.total_expenses = 0
        self.production = 1000
        self.events = []
        self.agents = []
        self.zone_names = ["ОФІС БОСА", "ВИРОБНИЦТВО", "ПЕРЕГОВОРНА", "СХОВИЩЕ"]
        self.zone_positions = [(170, 170), (510, 170), (170, 440), (510, 440)]
        self.zone_colors = ["#39445c", "#31564e", "#55456b", "#62513b"]

        self.sector_data = {
            "Цукерки": {"income": 1800, "salary": 250},
            "Одяг": {"income": 2200, "salary": 300},
            "Техніка": {"income": 3000, "salary": 400}
        }

        self.data = self.sector_data[sector]

        self.root.title("Factory Empire Simulator")
        self.root.geometry("1250x780")
        self.root.minsize(1050, 650)
        self.root.configure(bg="#171923")

        self.build_interface()
        self.add_event("🏭 Фабрика відкрила свої двері!")
        self.add_event(f"Обраний напрямок: {sector}")

        names = ["Олег", "Андрій", "Максим", "Іван", "Дмитро"]

        for name in names:
            self.create_agent(name, "Працівник", random.randrange(4), "#65e6a3")

        self.update_stats()
        self.animate_agents()
        self.update_simulation()

    def date_string(self):
        return f"{self.day:02d}.{self.month:02d}.{self.year}"

    def add_event(self, message):
        self.events.insert(0, f"[{self.date_string()}] {message}")
        self.events = self.events[:150]

        if hasattr(self, "event_list"):
            self.event_list.delete(0, tk.END)
            for event in self.events:
                self.event_list.insert(tk.END, event)

    def build_interface(self):
        header = tk.Frame(self.root, bg="#202638", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="FACTORY EMPIRE",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#202638"
        ).pack(side="left", padx=22)

        self.date_label = tk.Label(
            header,
            text="",
            font=("Arial", 13, "bold"),
            fg="#b8c5df",
            bg="#202638"
        )
        self.date_label.pack(side="left", padx=25)

        self.money_label = tk.Label(
            header,
            text="",
            font=("Arial", 16, "bold"),
            fg="#65e6a3",
            bg="#202638"
        )
        self.money_label.pack(side="right", padx=25)

        controls = tk.Frame(self.root, bg="#252c3d", height=48)
        controls.pack(fill="x")
        controls.pack_propagate(False)

        tk.Label(
            controls,
            text="ШВИДКІСТЬ СИМУЛЯЦІЇ:",
            font=("Arial", 10, "bold"),
            fg="#c5cee0",
            bg="#252c3d"
        ).pack(side="left", padx=15)

        for speed in range(1, 6):
            tk.Button(
                controls,
                text=f"{speed}x",
                command=lambda s=speed: self.set_speed(s),
                bg="#46536d",
                fg="white",
                activebackground="#687b9f",
                relief="flat",
                width=4
            ).pack(side="left", padx=3, pady=7)

        main = tk.Frame(self.root, bg="#171923")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        self.map_frame = tk.Frame(main, bg="#202638")
        self.map_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        map_header = tk.Frame(self.map_frame, bg="#202638")
        map_header.pack(fill="x", padx=15, pady=12)

        tk.Label(
            map_header,
            text="🏢 ТЕРИТОРІЯ ФАБРИКИ",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#202638"
        ).pack(side="left")

        self.map_canvas = tk.Canvas(
            self.map_frame,
            bg="#252e3b",
            highlightthickness=0
        )
        self.map_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.map_canvas.bind("<Configure>", self.draw_map)

        self.sidebar = tk.Frame(main, bg="#202638", width=330)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="📋 ПОДІЇ ФАБРИКИ",
            font=("Arial", 15, "bold"),
            fg="white",
            bg="#202638"
        ).pack(anchor="w", padx=15, pady=15)

        self.event_list = tk.Listbox(
            self.sidebar,
            bg="#171d2a",
            fg="#dce5f5",
            font=("Arial", 9),
            relief="flat",
            borderwidth=0,
            activestyle="none",
            selectbackground="#46536d",
            selectforeground="white"
        )
        self.event_list.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        self.stats = tk.Frame(self.root, bg="#202638", height=85)
        self.stats.pack(fill="x", side="bottom")
        self.stats.pack_propagate(False)

        self.stat_labels = {}

        stat_items = [
            ("Працівники", "workers"),
            ("Виробництво", "production"),
            ("Дохід за день", "income"),
            ("Витрати за день", "expenses"),
            ("Охорона", "security")
        ]

        for title, key in stat_items:
            box = tk.Frame(self.stats, bg="#2b3549", padx=15, pady=8)
            box.pack(side="left", fill="both", expand=True, padx=5, pady=9)

            tk.Label(
                box,
                text=title,
                font=("Arial", 9),
                fg="#aab8d0",
                bg="#2b3549"
            ).pack()

            label = tk.Label(
                box,
                text="",
                font=("Arial", 15, "bold"),
                fg="#65e6a3",
                bg="#2b3549"
            )
            label.pack()

            self.stat_labels[key] = label

    def draw_map(self, event=None):
        canvas = self.map_canvas
        canvas.delete("map")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width < 100 or height < 100:
            return

        canvas.create_rectangle(
            0, 0, width, height,
            fill="#293747",
            outline="",
            tags="map"
        )

        canvas.create_rectangle(
            20, 20, width - 20, height - 20,
            outline="#506078",
            width=3,
            tags="map"
        )

        positions = [
            (width * 0.27, height * 0.28),
            (width * 0.72, height * 0.28),
            (width * 0.27, height * 0.73),
            (width * 0.72, height * 0.73)
        ]

        self.zone_positions = positions

        canvas.create_line(
            positions[0][0], positions[0][1],
            positions[1][0], positions[1][1],
            positions[2][0], positions[2][1],
            positions[3][0], positions[3][1],
            fill="#8290a6",
            width=9,
            smooth=True,
            tags="map"
        )

        canvas.create_line(
            positions[0][0], positions[0][1],
            positions[2][0], positions[2][1],
            fill="#8290a6",
            width=9,
            tags="map"
        )

        canvas.create_line(
            positions[1][0], positions[1][1],
            positions[3][0], positions[3][1],
            fill="#8290a6",
            width=9,
            tags="map"
        )

        icons = ["🏢", "🏭", "🤝", "💰"]

        for i, (x, y) in enumerate(positions):
            color = self.zone_colors[i]

            canvas.create_rectangle(
                x - 105, y - 70,
                x + 105, y + 70,
                fill=color,
                outline="#aab8d0",
                width=2,
                tags="map"
            )

            canvas.create_text(
                x, y - 28,
                text=icons[i],
                font=("Arial", 27),
                fill="white",
                tags="map"
            )

            canvas.create_text(
                x, y + 20,
                text=self.zone_names[i],
                font=("Arial", 11, "bold"),
                fill="white",
                tags="map"
            )

        canvas.create_text(
            width / 2,
            25,
            text=f"ФАБРИКА: {self.sector.upper()}",
            font=("Arial", 11, "bold"),
            fill="#dce5f5",
            tags="map"
        )

        for agent in self.agents:
            self.create_agent_visual(agent)

    def create_agent(self, name, role, zone, color):
        x, y = self.zone_positions[zone]

        agent = {
            "name": name,
            "role": role,
            "zone": zone,
            "target": random.randrange(4),
            "x": x + random.randint(-35, 35),
            "y": y + random.randint(-20, 20),
            "color": color,
            "dot": None,
            "label": None
        }

        self.agents.append(agent)
        self.create_agent_visual(agent)

    def create_agent_visual(self, agent):
        canvas = self.map_canvas

        if agent["dot"] is not None:
            canvas.delete(agent["dot"])

        if agent["label"] is not None:
            canvas.delete(agent["label"])

        agent["dot"] = canvas.create_oval(
            agent["x"] - 7,
            agent["y"] - 7,
            agent["x"] + 7,
            agent["y"] + 7,
            fill=agent["color"],
            outline="white",
            width=1,
            tags="agent"
        )

        agent["label"] = canvas.create_text(
            agent["x"],
            agent["y"] - 19,
            text=agent["name"],
            fill="white",
            font=("Arial", 8, "bold"),
            tags="agent"
        )

    def animate_agents(self):
        if not self.root.winfo_exists():
            return

        for agent in self.agents:
            target_x, target_y = self.zone_positions[agent["target"]]

            target_x += random.uniform(-25, 25)
            target_y += random.uniform(-20, 20)

            dx = target_x - agent["x"]
            dy = target_y - agent["y"]
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 5:
                agent["target"] = random.randrange(4)
            else:
                step = min(1.8, distance)
                agent["x"] += dx / distance * step
                agent["y"] += dy / distance * step

            self.map_canvas.coords(
                agent["dot"],
                agent["x"] - 7,
                agent["y"] - 7,
                agent["x"] + 7,
                agent["y"] + 7
            )

            self.map_canvas.coords(
                agent["label"],
                agent["x"],
                agent["y"] - 19
            )

        self.root.after(40, self.animate_agents)

    def set_speed(self, speed):
        self.speed = speed
        self.add_event(f"⏩ Швидкість змінена на {speed}x")

    def update_stats(self):
        income = self.production * self.data["income"] // 1000
        expenses = self.workers * self.data["salary"]

        self.date_label.config(text=self.date_string())
        self.money_label.config(text=f"${self.money:,.0f}")

        self.stat_labels["workers"].config(text=str(self.workers))
        self.stat_labels["production"].config(text=f"{self.production:,}")
        self.stat_labels["income"].config(text=f"${income:,}")
        self.stat_labels["expenses"].config(text=f"${expenses:,}")
        self.stat_labels["security"].config(text=f"{self.security}/5")

    def next_day(self):
        self.day += 1

        days_in_month = calendar.monthrange(self.year, self.month)[1]

        if self.day > days_in_month:
            self.day = 1
            self.month += 1

            result = self.month_income - self.month_expenses

            if result >= 0:
                self.add_event(f"📈 Місячний прибуток: ${result:,}")
            else:
                self.add_event(f"📉 Місячний збиток: ${abs(result):,}")

            self.month_income = 0
            self.month_expenses = 0

            if self.month > 12:
                self.month = 1
                self.year += 1

    def random_worker_event(self):
        if random.randint(1, 100) <= 8 and self.workers < 50:
            names = ["Олександр", "Петро", "Сергій", "Віктор", "Роман", "Богдан"]
            name = random.choice(names)

            self.workers += 1
            self.create_agent(name, "Працівник", 0, "#65e6a3")
            self.add_event(f"👷 {name} влаштувався на роботу!")

        elif random.randint(1, 100) <= 7 and self.workers > 2:
            workers = [a for a in self.agents if a["role"] == "Працівник"]

            if workers:
                person = random.choice(workers)
                self.map_canvas.delete(person["dot"])
                self.map_canvas.delete(person["label"])
                self.agents.remove(person)
                self.workers -= 1
                self.add_event(f"🚪 {person['name']} звільнився!")

    def random_sponsor_event(self):
        if self.contract is None and random.randint(1, 100) <= 7:
            sponsors = [
                ("Global Industries", 1500),
                ("Mega Corporation", 2500),
                ("Future Holdings", 3500),
                ("United Partners", 5000),
                ("World Business Group", 7000)
            ]

            name, bonus = random.choice(sponsors)

            self.contract = {"name": name, "bonus": bonus}
            self.contract_days = random.randint(15, 45)

            self.create_agent(name, "Спонсор", 2, "#f4c76b")
            self.add_event(f"🤝 Спонсор {name} підписав контракт! Бонус ${bonus:,} на день")

        elif self.contract and random.randint(1, 100) <= 2:
            self.add_event(f"❌ Спонсор {self.contract['name']} розірвав контракт")
            self.contract = None
            self.contract_days = 0

            for agent in self.agents[:]:
                if agent["role"] == "Спонсор":
                    self.map_canvas.delete(agent["dot"])
                    self.map_canvas.delete(agent["label"])
                    self.agents.remove(agent)

    def security_event(self):
        chance = max(2, 18 - self.security * 3)

        if random.randint(1, 100) <= chance:
            stolen = min(self.money, random.randint(1000, 10000))
            self.money -= stolen
            self.month_expenses += stolen
            self.total_expenses += stolen
            self.add_event(f"🚨 Пограбування! Викрадено ${stolen:,}")

    def update_security(self):
        if self.money >= 500000:
            self.security = 5
        elif self.money >= 250000:
            self.security = 4
        elif self.money >= 100000:
            self.security = 3
        elif self.money >= 25000:
            self.security = 2
        else:
            self.security = 1

    def simulate_day(self):
        self.next_day()

        income = self.production * self.data["income"] // 1000
        expenses = self.workers * self.data["salary"]

        if self.contract:
            income += self.contract["bonus"]
            self.contract_days -= 1

            if self.contract_days <= 0:
                self.add_event(f"Контракт {self.contract['name']} завершився")
                self.contract = None

                for agent in self.agents[:]:
                    if agent["role"] == "Спонсор":
                        self.map_canvas.delete(agent["dot"])
                        self.map_canvas.delete(agent["label"])
                        self.agents.remove(agent)

        self.money += income - expenses
        self.month_income += income
        self.month_expenses += expenses
        self.total_income += income
        self.total_expenses += expenses

        self.random_worker_event()
        self.random_sponsor_event()
        self.security_event()
        self.update_security()
        self.update_stats()

    def update_simulation(self):
        for _ in range(self.speed):
            self.simulate_day()

        self.root.after(1000, self.update_simulation)


def launch(root, sector):
    for widget in root.winfo_children():
        widget.destroy()

    FactoryGame(root, sector)


def main():
    root = tk.Tk()
    root.title("Factory Empire Simulator")
    root.geometry("650x500")
    root.configure(bg="#171923")

    tk.Label(
        root,
        text="FACTORY EMPIRE",
        font=("Arial", 30, "bold"),
        fg="white",
        bg="#171923"
    ).pack(pady=(65, 10))

    tk.Label(
        root,
        text="Обери напрямок своєї майбутньої імперії",
        font=("Arial", 13),
        fg="#aab4d0",
        bg="#171923"
    ).pack(pady=10)

    for sector in ["Цукерки", "Одяг", "Техніка"]:
        tk.Button(
            root,
            text=sector,
            command=lambda s=sector: launch(root, s),
            font=("Arial", 16, "bold"),
            bg="#343d52",
            fg="white",
            activebackground="#52617e",
            activeforeground="white",
            relief="flat",
            width=25,
            pady=12
        ).pack(pady=10)

    tk.Label(
        root,
        text="Початок симуляції: 1 січня 2027 року",
        font=("Arial", 10),
        fg="#78849e",
        bg="#171923"
    ).pack(pady=25)

    root.mainloop()


if __name__ == "__main__":
    main()
