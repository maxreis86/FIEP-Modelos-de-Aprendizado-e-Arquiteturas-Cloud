const predictEndpoint = 'https://e147wyf0qj.execute-api.us-east-1.amazonaws.com/prod/get-predict?';
const saveEndpoint = 'https://lp1027iq13.execute-api.us-east-1.amazonaws.com/dev/get-predict?';
const commentEndpoint = 'https://gdq14tw3rl.execute-api.us-east-1.amazonaws.com/dev/post-comment?';
var count_execution = 0;

$('#Shap').hide();
$('#ProbLoader').hide();
$('#RatingLoader').hide();
$('#SuggestionLoader').hide();
$('#ShapLoader').hide();
$('#Comment').hide();
$('#LabelComment').hide();
$('#btnComment').hide();

// function printObject(o) {
//     var out = '';
//     for (var p in o) {
//       out += p + ': ' + o[p] + '\n';
//     }
//     alert(out);
//   }

function sendPredictionRequest() {

    $('#ProbGroup').hide();
    $('#RatingGroup').hide();
    $('#SuggestionGroup').hide();
    $('#Shap').hide();
    $('#Comment').hide();
    $('#LabelComment').hide();
    $('#btnComment').hide();

    $('#ProbLoader').show();
    $('#RatingLoader').show();
    $('#SuggestionLoader').show();
    
    if ($('#Imagem').val() == 'S') {
      $('#ShapLoader').show();
    }
    
    const linkedinUsername = (String(String(String($('#linkedinUsername').val().split("/").splice(-2))).replace(",", "")).trim())

    // alert('jobId=' + $('#jobId').val())
    // alert('linkedinUsername=' + linkedinUsername)
    // alert(predictEndpoint)
        
    $.ajax(
        {
           type:'GET',
           url: predictEndpoint,
           data: '&jobId=' + $('#jobId').val()  + '&linkedinUsername=' + linkedinUsername,
           success: function(data){
                // printObject(data)                
                $('#Prob').val(`${data.probability * 100}`.substring(0, 5)+'%');
                $('#Rating').val(data.rating);
                $('#Suggestion').val(data.suggestion);
           },
            error: function(error) {
                // printObject(error);
                // alert(error.statusCode);
                alert('Por favor, verifique o Linkedin. O endereço precisa ter uma barra no final como no exemplo: https://www.linkedin.com/in/sara-batista-166630176/');                
            },
            complete: function() {
                $('#ProbLoader').hide();
                $('#RatingLoader').hide();
                $('#SuggestionLoader').hide();
                $('#ProbGroup').show();
                $('#RatingGroup').show();
                $('#SuggestionGroup').show();
                $('#Comment').show();
                $('#LabelComment').show();
                $('#btnComment').show();                
                document.querySelector("#Comment").focus();
            }
        }
     );

     $.ajax(
        {
           type:'GET',
           url: saveEndpoint,
           data: 'jobId=' + $('#jobId').val()  + '&linkedinUsername=' + linkedinUsername,
           success: function(data){               
                $("#Shap").attr("src", `https://vagas-media.s3.amazonaws.com/sherlock/shapley/${data.image_path}`);
           },
            error: function(error) {
                $("#Shap").attr("src", "");
                $('#Shap').hide();
                $('#Comment').hide();
                $('#LabelComment').hide();
                $('#btnComment').hide();
                // alert('Por favor, verifique o Linkedin. O endereço precisa ter uma barra no final como no exemplo: https://www.linkedin.com/in/sara-batista-166630176/');                
            },
            complete: function() {
                $('#ShapLoader').hide();                
                if ($('#Imagem').val() == 'S') {
                  $('#Shap').show();
                }
            }
        }
     );
};


function sendCommentRequest() {

    const linkedinUsername = (String(String(String($('#linkedinUsername').val().split("/").splice(-2))).replace(",", "")).trim())    

    const comment = $('#Comment').val();

    if (comment == ''){
      if (count_execution == 0)
          {
            alert('O comentário não é obrigatório, mas ele vai te ajudar a lembrar detalhes desse talento ;-)');
          }
      count_execution++;
      $('#linkedinUsername').val('');
      $('#Comment').val('');
      $('#Shap').hide();
      $('#Comment').hide();
      $('#LabelComment').hide();
      $('#btnComment').hide();
      document.querySelector("#linkedinUsername").focus();
    }
    else {
        $.ajax(
          {
              type:'GET',
              url: commentEndpoint,
              data: 'jobId=' + $('#jobId').val()  + '&linkedinUsername=' + linkedinUsername   + '&comment=' + $('#Comment').val(),
            success: function(data){                
                  $('#linkedinUsername').val('');
                  $('#Comment').val('');      
                  $('#Shap').hide();
                  $('#Comment').hide();
                  $('#LabelComment').hide();
                  $('#btnComment').hide();
                  document.querySelector("#linkedinUsername").focus();
            },
              error: function(error) {
                  // printObject(error);
                  // alert(error.statusCode);
                  alert('Faça um comentário. Isso vai te ajudar a lembrar desse perfil!');
              },
              complete: function() {
                  // $('#linkedinUsername').val('');
                  // $('#Comment').val('');                
              }
          }
      );

    }
};

$('#btnPredictProb').click(sendPredictionRequest);
$('#btnComment').click(sendCommentRequest);

var input = document.getElementById("linkedinUsername");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("btnPredictProb").click();
  }
});

var input = document.getElementById("Comment");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("btnComment").click();
  }
});