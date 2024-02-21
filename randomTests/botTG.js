/* import 'dotenv/config'
require('dotenv').config() */
const ky = '7056648941:AAG_FCbKAFCKQp8tn1DpGBNRNXZvYzznyHk'
const { Bot, session, InlineKeyboard } = require("grammy");
const { Menu } = require("@grammyjs/menu");
const {
  conversations,
  createConversation,
} = require("@grammyjs/conversations");
//const apiky = process.env.API_TG;

const bot = new Bot(ky);

let qna = {
  "Budget": null,
  "Cavalli": null,
  "Consumi": null,
  "Cilindrata": null,
}

const userState = new Map();


  function session_collector() {
    return {}
  }

bot.use(session({
  initial: () => new session_collector()
}))
bot.use(conversations());

// register /mySession to show current session data
bot.command("mySession", (ctx) => {
  const session = ctx.session;
  ctx.reply(`Current session data: ${JSON.stringify(session)}`);
});

// convo function
async function collect_data_conv(conversation, ctx) {
  fields_to_collect = ["Budget",
                       "Cavalli",
                       "Consumi",
                       "Cilindrata"];
  const inlineKeyb = new InlineKeyboard()
  .text('Budget', 'Budget')
  .text('Cavalli', 'Cavalli')
  .text('Consumi', 'Consumi')
  .text('Cilindrata', 'Cilindrata');
  await ctx.reply("Quale dato vuoi inserire?", { reply_markup: inlineKeyb });

  for (let i = 0; i < fields_to_collect.length; i++) {
    let selected_field = await conversation.waitFor("callback_query");
    selected_field = selected_field.update.callback_query.data;
    ///
    await ctx.reply(`Inserisci il valore di ${selected_field}DA`);
    let value = await conversation.waitFor("message:text");
    value = value.message.text;
    ctx.session[`${selected_field}DA`] = value;
    await ctx.reply(`Il valore di ${selected_field} è ${value}`);
    ///
    await ctx.reply(`Inserisci il valore di ${selected_field}A`);
    value = await conversation.waitFor("message:text");
    value = value.message.text;
    ctx.session[`${selected_field}A`] = value;
    await ctx.reply(`Il valore di ${selected_field} è ${value}`);
    ///
  }
  await ctx.reply("Grazie per aver inserito i dati!");
  // send all the data
  
  await ctx.reply(`I dati inseriti sono: ${JSON.stringify(ctx.session)}`);
}
bot.use(createConversation(collect_data_conv));

// add /testino command for conversation
bot.command("menu", async (ctx) => {
  ctx.session = new session_collector();
  await ctx.conversation.enter("collect_data_conv");
});
bot.command("start", (ctx) => ctx.reply("Welcome! do /menu o/."));

bot.start();