/* import 'dotenv/config'
require('dotenv').config() */
const ky = '7056648941:AAG_FCbKAFCKQp8tn1DpGBNRNXZvYzznyHk'
const { Bot } = require("grammy");
const { Menu } = require("@grammyjs/menu");

//const apiky = process.env.API_TG;

const bot = new Bot(ky);

let qna = {
  "Domanda1": null,
  "Domanda2": null,
  "Domanda3": null,
  "Domanda4": null,
}

const userState = new Map();

// Function to handle the user's response to "Domanda1"
function handleDomanda1Response(ctx) {
  const userId = ctx.from.id;
  const userResponse = ctx.message.text;

  if (userState.has(userId) && userState.get(userId) === 'waiting_for_domanda1_response') {
    ctx.reply(`You responded with: ${userResponse}`);
    userState.delete(userId);
  }
}

function rispOne(ctx) {
  const userId = ctx.from.id;
  if (!userState.has(userId)) {
    userState.set(userId, 'waiting_for_domanda1_response');
    ctx.reply("Domanda1:");
  } else {
    ctx.reply("Please complete your current task before starting a new one.");
  }
}

const menu = new Menu("my-menu-identifier")
  .text("AA", (ctx) => {
    rispOne(ctx);
  })
  .text("A", (ctx) => ctx.reply("You pressed A!")).row()
  .text("BB", (ctx) => ctx.reply("You pressed BB!"))
  .text("B", (ctx) => ctx.reply("You pressed B!")).row();

// Register the menu and message handling middleware
bot.use(menu);
bot.command("start", (ctx) => ctx.reply("Welcome! do /menu o/."));
bot.command("menu", (ctx) => {
  ctx.reply("Welcome! do quclsoa mortaccitua o/.", { reply_markup: menu })
  
});
bot.on('message', handleDomanda1Response);




bot.start();