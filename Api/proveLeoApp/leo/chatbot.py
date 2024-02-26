#attraverso tutorial Medium : https://medium.com/@mailsushmita.m/create-an-generative-ai-chatbot-using-python-and-flask-a-step-by-step-guide-ea39439cf9ed
# import openai

# openai.api_key  = "<place your openai_api_key>"


 # def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]
#
#
#
#  @app.route("/get")
# def get_bot_response():
#     userText = request.args.get('msg')
#     response = get_completion(userText)
#     #return str(bot.get_response(userText))
#     return response
#
#
#
#
#
#        html style
##chatbox {
      #   margin-left: auto;
      #   margin-right: auto;
      #   width: 40%;
      #   margin-top: 60px;
      # }
      # #userInput {
      #   margin-left: auto;
      #   margin-right: auto;
      #   width: 40%;
      #   margin-top: 60px;
      # }
      # #textInput {
      #   width: 90%;
      #   border: none;
      #   border-bottom: 3px solid black;
      #   font-family: monospace;
      #   font-size: 17px;
      # }
      # .userText {
      #   color: white;
      #   font-family: monospace;
      #   font-size: 17px;
      #   text-align: right;
      #   line-height: 30px;
      # }
      # .userText span {
      #   background-color: #808080;
      #   padding: 10px;
      #   border-radius: 2px;
      # }
      # .botText {
      #   color: white;
      #   font-family: monospace;
      #   font-size: 17px;
      #   text-align: left;
      #   line-height: 30px;
      # }
      # .botText span {
      #   background-color: #4169e1;
      #   padding: 10px;
      #   border-radius: 2px;
      # }
      # #tidbit {
      #   position: absolute;
      #   bottom: 0;
      #   right: 0;
      #   width: 300px;
      # }
      # .boxed {
      #   margin-left: auto;
      #   margin-right: auto;
      #   width: 78%;
      #   margin-top: 60px;
      #   border: 1px solid green;
      # }
#
#        script chat
#                   <script>
#                 function getBotResponse() {
#                     var rawText = $("#textInput").val();
#                     var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
#                     $("#textInput").val("");
#                     $("#chatbox").append(userHtml);
#                     document
#                         .getElementById("userInput")
#                         .scrollIntoView({ block: "start", behavior: "smooth" });
#                     $.get("/get", { msg: rawText }).done(function (data) {
#                         var botHtml = '<p class="botText"><span>' + data + "</span></p>";
#                         $("#chatbox").append(botHtml);
#                         document
#                             .getElementById("userInput")
#                             .scrollIntoView({ block: "start", behavior: "smooth" });
#                     });
#                 }
#                 $("#textInput").keypress(function (e) {
#                     if (e.which == 13) {
#                         getBotResponse();
#                     }
#                 });
#                </script>