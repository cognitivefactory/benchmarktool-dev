jQuery(document).ready(function ($) {

    
    function check_training_parameters(form_id, form_inputs){
        
        var value, input_type, input_valid_values, input_correct;
        var form_correct = true;
        
        var obj = new Object();
        obj["library"] = form_id.split("_")[0];
        
        //check each input values
        for (i = 0; i < form_inputs.length; i++) {
            input_correct = true;
            value = form_inputs[i]['value'].trim();

            if(value.length==0){
                //console.log("empty value");
                input_correct = false;
                form_correct = false;
            }
            else{
                
                input_type = $("input[name='"+form_inputs[i]['name']+"'").attr('input_type');
                input_valid_values = input_type.split("|")
    
                //if the input value needs to be a specified values
                if(input_valid_values.length !== 1){
                    
                    if(input_valid_values.indexOf(value) == -1){
                        //console.log("if value not in the list of specified values");
                        input_correct = false;
                        form_correct = false;
                    }
                }
                else{
                    switch(input_type){
                        
                        //if int or float
                        case("int"):
                        case("float"):
                        //console.log(value + " should be a number");
                        /*
                        +value==+value :
                        returns true if the string is a valid number
                        ex : "12" -> true, "test" -> false, 12 -> true
                        */
                       if(!(+value==+value)){
                           //console.log("not a number");
                           input_correct = false;
                           form_correct = false;
                        }
                        let number = new Number(value);
                        
                        if(input_type == "int"){
                            
                            //if value == float
                            if(number%1 != 0){
                                    //console.log("not an int");
                                    input_correct = false;
                                    form_correct = false;
                                }
                            }
                            
                            break;
                            
                            
                            case "string":
                                //console.log(value + " should be a string");
                                
                                if(+value==+value){
                                    //console.log("value == number");
                                    input_correct = false;
                                    form_correct = false;
                                }
                                break;
                                
                                case "boolean":
                                    //console.log(value + "s hould be a boolean");
                                    
                                    if(value != "true" && value != "false"){
                                        //console.log("not equal true or false");
                                        
                                        input_correct = false;
                                        form_correct = false;
                                    }
                                    
                                    break;
    
                                    default:
                                        input_correct = false;
                                        form_correct = false;
                                        
                                        break;
                                    }
                                }
                            } 
                            
            if(!input_correct){
                $('#' + form_id + "_" + form_inputs[i]['name'] + '_error').text("Format incorrect. Type requis = " + input_type.toString());
            }
            else{
                
                //if valid input, append obj
                //format : [[param_name : value]] 
                obj[form_inputs[i]['name']] = value;

                //update the display in case an error has been corrected
                $('#' + form_id + "_" + form_inputs[i]['name'] + '_error').text("");
            }
        }
        
        if(form_correct){
            return obj;
        }
        else{
            return false;
        }
    }

    
    var socket = io.connect('http://' + document.domain + ':' + location.port);


    ////////////
    /// DATA_TRAIN.HTML

    socket.on('connect', function () {
        
        //send training parameters
        $('.data').on('click', function(){
            socket.emit('select_train_data', {
                filename: $(this).attr('filename') + ".json"
            })
        })
    });

    //event = selected
    socket.on('selected_train_data', function (msg) {
        if(msg==1){
            alert("Fichier de données d'entraînement sélectionné");
            setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
        }
        else{
            alert("Erreur, veuillez choisir un fichier de données");
        }
    })



    
    ////////////
    /// MODELS.HTML

    // Check training data parameters
    socket.on('connect', function () {
        
        //send training parameters
        $('.training_form').on('submit', function (e) {
            e.preventDefault()

            var data = $(this).serializeArray();
            var obj = new Object();
            obj = check_training_parameters($(this).attr('id'), data);
            
            
            if(obj != false){
                socket.emit('start_training', {
                    options:obj,
                })
            }else{
                console.log("error");
            }
            
        })
    });
    
    //event = training 
    socket.on('training', function (msg) {
        console.log('-----training');

        content = $('[popup_name="popup_start"] > .popup_content');
        content.children().hide();

        if(msg!=1){
            content.append("<h1>Jeu de données d'entraînement vide</h1>")
            content.append("<p>Veuillez sélection un jeu de données d'entraînement</p>");
            setTimeout(function () { window.location = window.origin + '/data_train'; }, 2000);
        }else{
            content.append("<h1>Démarrage de l'entraînement<h1>");
            setTimeout(function () { window.location = window.origin + '/models'; }, 2000);
        }
    })

    //event = training_done
    socket.on('training_done', function (msg) {
        alert("entrainement terminé.");
    })

});