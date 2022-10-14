const predictEndpoint = 'https://5a51rpxvrj.execute-api.us-east-1.amazonaws.com/prod/get-predict?';
// const predictEndpoint = 'https://5a51rpxvrj.execute-api.us-east-1.amazonaws.com/prod/get-predict?';

$('#ProbLoader').hide();
$('#RatingLoader').hide();
$('#PredictLoader').hide();

function sendPredictionRequest() {

    $('#ProbGroup').hide();
    $('#RatingGroup').hide();
    $('#PredictGroup').hide();
    
    $('#ProbLoader').show();
    $('#RatingLoader').show();
    $('#PredictLoader').show();
        
    $.ajax(
        {
           type:'GET',
           url: predictEndpoint,
           data: '&passenger_id=' + $('#passenger_id').val(),
           // data: '&passenger_id=' + $('#passenger_id').val()  + '&embarked=' + $('#embarked').val(),
           success: function(data){
               
               if (data.message == 'Prediction executed successfully!') {
                   
                    $('#Prob').val(`${data.probability * 100}`.substring(0, 5)+'%');
                    $('#Rating').val(data.rating);
                    $('#Predict').val(data.predict);

                    $('#ProbLoader').hide();
                    $('#RatingLoader').hide();
                    $('#PredictLoader').hide();

                    $('#ProbGroup').show();
                    $('#RatingGroup').show();
                    $('#PredictGroup').show();
               }
               else {
                   $('#Prob').val('');
                   $('#Rating').val('');
                   $('#Predict').val('');
                   alert('Passenger_id not found');
               }
           },
            error: function(error) {
                $('#Prob').val('');
                $('#Rating').val('');
                $('#Predict').val('');
                alert('Passenger_id not found');
            },
            complete: function() {
                $('#ProbLoader').hide();
                $('#RatingLoader').hide();
                $('#PredictLoader').hide();
                $('#ProbGroup').show();
                $('#RatingGroup').show();
                $('#PredictGroup').show();
                document.querySelector("#passenger_id").focus();
            }
        }
     );
};

$('#btnPredictProb').click(sendPredictionRequest);

var input = document.getElementById("passenger_id");
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("btnPredictProb").click();
  }
});