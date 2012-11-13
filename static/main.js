$(document).ready(function() {
    var ui = $('body')
    var text = 'welcome to azeroth!';

    var display = $('<div></div>');
    display.text(text);
    ui.append(display);

    var receive = function(o) {
    display.text(display.text + o);
    input.text('');
    }

    var send = function() {
    $.getJSON('play', input.text, receive);    
    }

    var input = $('<input type = "text" />');
    input.submit(function() {
      console.log('submit called');
      send() 
      });

    ui.append(input);
    input.submit();
});
