/* import 'dotenv/config'
require('dotenv').config() */
const ky = '7056648941:AAG_FCbKAFCKQp8tn1DpGBNRNXZvYzznyHk'
const { Bot, session, InlineKeyboard, InlineQueryResultBuilder } = require("grammy");
const { Menu } = require("@grammyjs/menu");
const {
  conversations,
  createConversation,
} = require("@grammyjs/conversations");
//const apiky = process.env.API_TG;

const bot = new Bot(ky);

let qna = {
  "Quale e' il tuo Budget?": 'prezzo',
  "Quanti Cavalli minimo?": 'cavalli',
  "Massimo Consumi 100km?": 'consumi',
  "Cilindrata minima?": 'cilindrata',
  //"Emissioni massime?": 'emissioni',
}

a = {'marchio': 'tutti', 'carburante': 'tutti ', 'consumi': 0, 'emissioni': 0, 'prezzo': 0, 'serbatoio': 0, 'potenza': 0, 'cilindrata': 0, 'cavalli': 0} 
b = {'marchio': false, 'carburante': false, 'consumi': false, 'emissioni': false, 'prezzo': false, 'serbatoio': false, 'potenza': false, 'cilindrata': false, 'cavalli': false}


const userState = new Map();


  function session_collector() {
    return {'settings':{'marchio': 'tutti', 'carburante': 'tutti ', 'consumi': 0, 'emissioni': 0, 'prezzo': 0, 'serbatoio': 0, 'potenza': 0, 'cilindrata': 0, 'cavalli': 0},'clicked':b}
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
    if (val=='prezzo'){
      console.log("eeE",parseInt(e))
      return parseInt(e);
    }
    else if(val == 'cavalli'){
      return parseInt(e);
    }
    else if(val == 'consumi'){
      return parseFloat(e);
    }
    else if(val == 'cilindrata'){
      return parseFloat(e);
    }
  }catch (err){
    console.log("mmm?",err)
    return false;
  }
}

async function validateAnswer(a,val){
  oldA = a;
  a = tryConvert(a,val)
  if (val=='prezzo'){
    if (typeof(a)==='number' && Number.isInteger(a) ){
        return true;
    }
  }
  else if(val == 'cavalli'){
      if (typeof(a)==='number' && Number.isInteger(a) ){
          return true;
      }
  }
  else if(val == 'consumi'){
      if (typeof(a)==='number' && oldA.includes('.')){
          return true;
      }
  }
  else if(val == 'cilindrata'){
      if (typeof(a)==='number' && oldA.includes('.')){
          return true;
      }
  }
  
  return false;
}


async function getshowC(ctx){
  await ctx.reply(`I dati inseriti sono: ${JSON.stringify(ctx.session['settings'])}`);
  let res = await fetch('http://127.0.0.1:5000/api/auto_filter', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(ctx.session['settings']),
  })
  res = await res.json()
  
  slicedRes = res['data']
  if (res['data'].length > 10){
    slicedRes = res['data'].slice(0,10)
  }


  if (res['success']){
    await ctx.reply(`Ecco ${slicedRes.length}/${res['data'].length} macchine che soddifano i tuoi criteri`);
  }
  else{
    await ctx.reply(`0 Macchine trovate`);
    return 
  }
  
  for (const element of slicedRes) {
    msg = `
    <a href="${element['foto_auto']}">${element['modello']}</a>
    Marca: ${element['nome']}
    Prezzo: ${element['prezzo']}$
    Cilindrata: ${element['cilindrata']}L
    Potenza: ${element['potenza']}kw
    Cavalli: ${element['cavalli']}cv
    Carburante: ${element['carburante']}
    Consumi: ${element['consumi']}L/100km
    Emissioni: ${element['emissioni']}g/km
    Serbatoio: ${element['serbatoio']}L
    `
    console.log("meeeessssaggiuss",msg)
    //await ctx.replyWithPhoto({ url: `${element['foto_auto']}` }, { caption: msg });
    
    await ctx.reply(msg,{ parse_mode: 'HTML' });
  };
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
    ctx.session['settings'][value.toLowerCase()] = valuez;
  }
  console.log("sesssione ctx setting",ctx.session['settings'])
  await getshowC(ctx)
  
}
bot.use(createConversation(collect_data_conv));


const buttonRow = Object.entries(b).map(([label, data]) => InlineKeyboard.text(label, data));
const keyboard = InlineKeyboard.from([buttonRow]);


bot.command("start", async (ctx) => {
  //ctx.session = new session_collector();
  let a =await ctx.conversation.enter("collect_data_conv");
});
bot.command("settings", (ctx) => {
  ctx.reply("Welcome! seelziona i parametri per la tua auto"), { reply_markup: keyboard }});

bot.start();

