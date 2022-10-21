from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import os


def main():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    def button_1_command():
        arc= open("env.txt", "w")
        arc.write(entry_3.get())
        arc.close()

        acr = open("envpuerto.txt", "w")
        acr.write(entry_2.get())
        acr.close()

        car = open("user.txt", "w")
        car.write(entry_1.get())
        car.close()

    def button_2_command():
        window.destroy()
        os.system("main_Asteroides.py")

    

    window = Tk()

    window.geometry("375x650")
    window.configure(bg = "#AE9F9F")


    canvas = Canvas(
        window,
        bg = "#AE9F9F",
        height = 650,
        width = 375,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        31.000000000000007,
        20.000000000000057,
        344.0,
        93.00000000000006,
        fill="#BBBBBB",
        outline="")

    canvas.create_rectangle(
        58.00000000000001,
        112.00000000000006,
        318.0,
        603.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        191.0,
        403.50000000000006,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_1.place(
        x=76.0,
        y=386.00000000000006,
        width=230.0,
        height=33.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        191.0,
        304.50000000000006,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_2.place(
        x=76.0,
        y=287.00000000000006,
        width=230.0,
        height=33.0
    )

    canvas.create_text(
        122.0,
        348.00000000000006,
        anchor="nw",
        text="Ingresa tu nombre:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        191.0,
        192.50000000000006,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_3.place(
        x=76.0,
        y=175.00000000000006,
        width=230.0,
        height=33.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: button_1_command(),
        relief="flat"
    )
    button_1.place(
        x=130.0,
        y=454.00000000000006,
        width=115.0,
        height=32.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: button_2_command(),
        relief="flat"
    )
    button_2.place(
        x=103.0,
        y=507.00000000000006,
        width=169.0,
        height=58.0
    )

    canvas.create_text(
        80.0,
        240.00000000000006,
        anchor="nw",
        text="Ingresar puerto del servidor:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        93.0,
        137.00000000000006,
        anchor="nw",
        text="Ingresa la ip del servidor:",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        106.0,
        42.00000000000006,
        anchor="nw",
        text="Asteroid - 5IV7",
        fill="#000000",
        font=("Inter Medium", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()





if __name__ == "__main__":
    main()