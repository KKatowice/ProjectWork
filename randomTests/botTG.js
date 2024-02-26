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
  "Quale e' il tuo Budget?": 'Budget',
  "Quanti Cavalli minimo?": 'Cavalli',
  "Massimo Consumi 100km?": 'Consumi',
  "Cilindrata minima?": 'Cilindrata',
}
let qna_settings = {
  'Budget':false,
  'Cavalli':false,
  'Consumi':false,
  'Cilindrata':false,
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


function tryConvert(e,val){
  console.log("in tryconv",e,val, typeof(e))
  try{
    if (val=='Budget'){
      console.log("eeE",parseInt(e))
      return parseInt(e);
    }
    else if(val == 'Cavalli'){
      return parseInt(e);
    }
    else if(val == 'Consumi'){
      return parseFloat(e);
    }
    else if(val == 'Cilindrata'){
      return parseFloat(e);
    }
  }catch (err){
    console.log("mmm?",err)
    return false;
  }
}

async function validateAnswer(a,val){
  console.log(a,"1aa",val)
  oldA = a;
  a = tryConvert(a,val)
  console.log(a,"2aa", typeof(a))
  if (val=='Budget'){
    if (typeof(a)==='number' && Number.isInteger(a) && a > 1000){
        return true;
    }
}
else if(val == 'Cavalli'){
    if (typeof(a)==='number' && Number.isInteger(a) && a > 0){
        return true;
    }
}
else if(val == 'Consumi'){
    if (typeof(a)==='number' && oldA.includes('.') && a > 0){
        return true;
    }
}
else if(val == 'Cilindrata'){
    if (typeof(a)==='number' && oldA.includes('.') && a > 0){
        return true;
    }
}
  
  return false;
}


async function getshowC(ctx){
  await ctx.reply(`I dati inseriti sono: ${JSON.stringify(ctx.session)}`);
  let res = await fetch('http://127.0.0.1:5000/api/auto_filter', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(ctx.session),
  })
}



// convo function
async function collect_data_conv(conversation, ctx) {
  await ctx.reply(`Benvenuto in DrivenChoice Bot [scrivi /stop per bloccarmi]`);
  for (const [key, value] of Object.entries(qna)) {
    await ctx.reply(key);
    let valuez = await conversation.waitFor("message:text");
    valuez = valuez.message.text;
    val = await validateAnswer(valuez,value)
    while (!val){
      console.log("isvalid", val)
      await ctx.reply(`Inserisci un valore valido per ${value}`);
      valuez = await conversation.waitFor("message:text");
      valuez = valuez.message.text;
      console.log(valuez,value)
      if (valuez == '/stop'){
        await ctx.reply(`Stopping`);
        return}
      val = await validateAnswer(valuez, value)
    }
    ctx.session[value.toLowerCase()] = valuez;
  }
  console.log(ctx.session)
 getshowC(ctx)
  
}
bot.use(createConversation(collect_data_conv));


const buttonRow = qna_settings
  .map(([label, data]) => InlineKeyboard.text(label, data));
const keyboard = InlineKeyboard.from([buttonRow]);


bot.command("start", async (ctx) => {
  //ctx.session = new session_collector();
  let a =await ctx.conversation.enter("collect_data_conv");
});
bot.command("settings", (ctx) => {
  ctx.reply("Welcome! seelziona i parametri per la tua auto"), { reply_markup: keyboard }});

bot.start();













/* async function collect_data_conv(conversation, ctx) {
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
} */