import { config } from "dotenv";
config();

const MESSAGE = "Hello from HackMIT!";
const POKE_API_KEY = process.env.POKE_API_KEY;

async function sendRequest() {
  try {
    const response = await fetch(
      "https://poke.com/api/v1/inbound-sms/webhook",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${POKE_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: MESSAGE }),
      }
    );

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Error sending request:", error);
  }
}

sendRequest();
