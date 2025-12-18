#!/usr/bin/env python3
import asyncio
import sys
import os
from tapo import ApiClient

EMAIL = os.getenv("TAPO_EMAIL", "avi.rohit13@gmail.com")
PASSWORD = os.getenv("TAPO_PASSWORD", "Lumia@123")
BULB_IP = os.getenv("BULB_IP", "192.168.1.18")

# Preset colors (hue, saturation)
COLORS = {
    "red": (0, 100),
    "orange": (30, 100),
    "yellow": (60, 100),
    "green": (120, 100),
    "cyan": (180, 100),
    "blue": (240, 100),
    "purple": (270, 100),
    "pink": (300, 100),
    "white": (0, 0),
}

async def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    value = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        client = ApiClient(EMAIL, PASSWORD)
        device = await client.l530(BULB_IP)
        info = await device.get_device_info()
        name = info.nickname

        # === POWER CONTROLS ===
        if command == "on":
            await device.on()
            print(f"✓ {name} turned ON")

        elif command == "off":
            await device.off()
            print(f"✓ {name} turned OFF")

        elif command == "toggle":
            if info.device_on:
                await device.off()
                print(f"✓ {name} turned OFF")
            else:
                await device.on()
                print(f"✓ {name} turned ON")

        # === BRIGHTNESS ===
        elif command == "brightness" or command == "b":
            if not value or not value.isdigit():
                print(f"Current brightness: {info.brightness}%")
                print("Usage: python bulb.py brightness <1-100>")
                return
            level = max(1, min(100, int(value)))
            await device.set_brightness(level)
            print(f"✓ {name} brightness set to {level}%")

        # === COLOR (hue,saturation) ===
        elif command == "color" or command == "c":
            if not value:
                print("Usage: python bulb.py color <name|hue,sat>")
                print(f"Available colors: {', '.join(COLORS.keys())}")
                print("Or use hue,saturation: 0,100 (red) to 360,100")
                return

            if value.lower() in COLORS:
                hue, sat = COLORS[value.lower()]
            elif "," in value:
                hue, sat = map(int, value.split(","))
            else:
                print(f"Unknown color: {value}")
                print(f"Available: {', '.join(COLORS.keys())}")
                return

            await device.set_hue_saturation(hue, sat)
            print(f"✓ {name} color set to hue:{hue}, saturation:{sat}")

        # === COLOR TEMPERATURE (warm to cool white) ===
        elif command == "temp" or command == "t":
            if not value or not value.isdigit():
                print("Usage: python bulb.py temp <2500-6500>")
                print("  2500 = Warm white (candle)")
                print("  4000 = Neutral white")
                print("  6500 = Cool white (daylight)")
                return
            temp = max(2500, min(6500, int(value)))
            await device.set_color_temperature(temp)
            print(f"✓ {name} temperature set to {temp}K")

        # === PRESET SCENES ===
        elif command == "warm":
            await device.set_color_temperature(2700)
            await device.set_brightness(50)
            print(f"✓ {name} set to warm mode")

        elif command == "cool":
            await device.set_color_temperature(6500)
            await device.set_brightness(100)
            print(f"✓ {name} set to cool daylight mode")

        elif command == "night":
            await device.set_color_temperature(2500)
            await device.set_brightness(10)
            print(f"✓ {name} set to night mode")

        elif command == "reading":
            await device.set_color_temperature(4000)
            await device.set_brightness(80)
            print(f"✓ {name} set to reading mode")

        elif command == "movie":
            await device.set_hue_saturation(30, 80)
            await device.set_brightness(20)
            print(f"✓ {name} set to movie mode")

        elif command == "party":
            await device.set_hue_saturation(280, 100)
            await device.set_brightness(100)
            print(f"✓ {name} set to party mode (purple)")

        # === DEVICE INFO ===
        elif command == "status" or command == "s":
            usage = await device.get_device_usage()
            print(f"\n{'='*35}")
            print(f"  {name}")
            print(f"{'='*35}")
            print(f"  Power:       {'ON' if info.device_on else 'OFF'}")
            print(f"  Brightness:  {info.brightness}%")
            print(f"  Model:       {info.model}")
            print(f"  IP:          {BULB_IP}")
            print(f"{'='*35}")
            print(f"  Usage Today:     {usage.today_runtime} min")
            print(f"  Usage This Month: {usage.month_runtime} min")
            print(f"{'='*35}\n")

        elif command == "info":
            info_json = await device.get_device_info_json()
            print(info_json)

        # === DEVICE MANAGEMENT ===
        elif command == "reboot":
            confirm = input("Reboot the bulb? (yes/no): ")
            if confirm.lower() == "yes":
                await device.device_reboot()
                print(f"✓ {name} is rebooting...")
            else:
                print("Cancelled")

        elif command == "reset":
            confirm = input("⚠️  FACTORY RESET? This will unpair the bulb! (yes/no): ")
            if confirm.lower() == "yes":
                await device.device_reset()
                print(f"✓ {name} factory reset initiated")
            else:
                print("Cancelled")

        # === HELP ===
        elif command == "help" or command == "h":
            print("""
╔═══════════════════════════════════════════════════════════╗
║              TAPO L530 BULB CONTROL                       ║
╠═══════════════════════════════════════════════════════════╣
║  POWER                                                    ║
║    on                    Turn on                          ║
║    off                   Turn off                         ║
║    toggle                Toggle on/off                    ║
║                                                           ║
║  BRIGHTNESS                                               ║
║    brightness <1-100>    Set brightness level             ║
║    b <1-100>             (shortcut)                       ║
║                                                           ║
║  COLOR                                                    ║
║    color <name>          Set preset color                 ║
║    color <hue,sat>       Set custom color (0-360, 0-100)  ║
║    c <name|hue,sat>      (shortcut)                       ║
║                                                           ║
║    Preset colors: red, orange, yellow, green, cyan,       ║
║                   blue, purple, pink, white               ║
║                                                           ║
║  COLOR TEMPERATURE                                        ║
║    temp <2500-6500>      Set white temperature            ║
║    t <2500-6500>         (shortcut)                       ║
║      2500 = Warm/Candle                                   ║
║      4000 = Neutral                                       ║
║      6500 = Cool/Daylight                                 ║
║                                                           ║
║  PRESET SCENES                                            ║
║    warm                  Warm cozy light                  ║
║    cool                  Bright daylight                  ║
║    night                 Dim night light                  ║
║    reading               Neutral reading light            ║
║    movie                 Dim warm ambiance                ║
║    party                 Bright purple                    ║
║                                                           ║
║  DEVICE                                                   ║
║    status / s            Show bulb status & usage         ║
║    info                  Raw device info (JSON)           ║
║    reboot                Reboot the bulb                  ║
║    reset                 Factory reset (unpairs!)         ║
╚═══════════════════════════════════════════════════════════╝

Examples:
  python bulb.py on
  python bulb.py b 75
  python bulb.py color red
  python bulb.py color 180,50
  python bulb.py temp 3000
  python bulb.py movie
""")
        else:
            print(f"Unknown command: {command}")
            print("Run 'python bulb.py help' for available commands")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
