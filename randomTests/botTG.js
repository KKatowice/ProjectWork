/* import 'dotenv/config'
require('dotenv').config() */
const ky = '7056648941:AAG_FCbKAFCKQp8tn1DpGBNRNXZvYzznyHk'
const { Bot } = require("grammy");
const { Menu } = require("@grammyjs/menu");

//const apiky = process.env.API_TG;

const bot = new Bot(ky);

bot.command("start", (ctx) => ctx.reply("Welcome! do /menu o/."));

const userState = new Map();

function handleDomanda1Response(ctx) {
  const userId = ctx.from.id;
  const userResponse = ctx.message.text;

  if (userState.has(userId) && userState.get(userId) === 'domanda1_response') {
    ctx.reply(`You responded with: ${userResponse}`);
    userState.delete(userId);
  }
}

function rispOne(ctx) {
  const userId = ctx.from.id;
  if (!userState.has(userId)) {
    userState.set(userId, 'domanda1_response');
    ctx.reply("Domanda1:");
  } else {
    ctx.reply("Please complete your current task before starting a new one.");
  }
}

const menu = new Menu("Menu Scelta")
  .text("Budget", (ctx) => {
    rispOne(ctx);
  }) // da a
  .text("Cavalli", (ctx) => ctx.reply("You pressed A!")).row() // da a
  .text("Cilindrata", (ctx) => ctx.reply("You pressed BB!")) // da a
  .text("Consumi", (ctx) => ctx.reply("You pressed B!")).row() // da a
  //.text("Marchi", (ctx) => ctx.reply("You pressed BB!")) @TODO menu con tutti i marchi

bot.use(menu);
bot.on('message', handleDomanda1Response);

bot.command("menu", async (ctx) => {
    await ctx.reply("Impostazioni:", { reply_markup: menu });
  });


bot.start();