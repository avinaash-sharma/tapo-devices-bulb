require("dotenv").config();
const { cloudLogin, loginDeviceByIp } = require("tp-link-tapo-connect");

const EMAIL = process.env.TAPO_EMAIL;
const PASSWORD = process.env.TAPO_PASSWORD;
const BULB_IP = process.env.BULB_IP;

const command = process.argv[2];
const value = process.argv[3];

async function main() {
  try {
    console.log("Connecting to bulb...");
    const device = await loginDeviceByIp(EMAIL, PASSWORD, BULB_IP);

    // Get device info
    const info = await device.getDeviceInfo();

    switch (command) {
      case "on":
        await device.turnOn();
        console.log(`${info.nickname} turned ON`);
        break;

      case "off":
        await device.turnOff();
        console.log(`${info.nickname} turned OFF`);
        break;

      case "toggle":
        if (info.device_on) {
          await device.turnOff();
          console.log(`${info.nickname} turned OFF`);
        } else {
          await device.turnOn();
          console.log(`${info.nickname} turned ON`);
        }
        break;

      case "brightness":
        if (!value || isNaN(value)) {
          console.log("Usage: node bulb.js brightness <1-100>");
          return;
        }
        await device.setBrightness(parseInt(value));
        console.log(`${info.nickname} brightness set to ${value}%`);
        break;

      case "color":
        // For L530 color bulbs - value format: "hue,saturation"
        if (!value) {
          console.log("Usage: node bulb.js color <hue>,<saturation>");
          console.log("  hue: 0-360, saturation: 0-100");
          console.log("  Examples: 0,100 (red), 120,100 (green), 240,100 (blue)");
          return;
        }
        const [hue, sat] = value.split(",").map(Number);
        await device.setColour(hue, sat);
        console.log(`${info.nickname} color set to hue:${hue}, saturation:${sat}`);
        break;

      case "status":
      default:
        console.log("\n--- Bulb Status ---");
        console.log(`Name: ${info.nickname}`);
        console.log(`Power: ${info.device_on ? "ON" : "OFF"}`);
        console.log(`Brightness: ${info.brightness || "N/A"}%`);
        console.log(`Model: ${info.model}`);
        console.log(`IP: ${BULB_IP}`);

        if (!command || command === "status") break;

        console.log("\n--- Available Commands ---");
        console.log("  node bulb.js on            - Turn on");
        console.log("  node bulb.js off           - Turn off");
        console.log("  node bulb.js toggle        - Toggle on/off");
        console.log("  node bulb.js brightness 50 - Set brightness (1-100)");
        console.log("  node bulb.js color 240,100 - Set color (L530 only)");
        console.log("  node bulb.js status        - Show status");
        break;
    }
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}

main();
