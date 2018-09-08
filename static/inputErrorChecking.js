document.addEventListener('DOMContentLoaded', () => {

  // by default submit button is disabled
  document.getElementById('submit').disabled = true;
  document.getElementById('msg_submit').disabled = true;

  // Enable button only if there is text in the input field
  document.getElementById('channel_name').onkeyup = () => {
        var my_string = document.getElementById('channel_name').value;
        var spaceCount = (my_string.split(" ").length - 1);
        if (document.getElementById('channel_name').value.length != spaceCount)
            document.getElementById('submit').disabled = false;
        else
            document.getElementById('submit').disabled = true;
    };
  // Enable button only if there is text in the input field
  document.getElementById('message_text').onkeyup = () => {
        var my_string = document.getElementById('message_text').value;
        var spaceCount = (my_string.split(" ").length - 1);
        if (document.getElementById('message_text').value.length != spaceCount)
            document.getElementById('msg_submit').disabled = false;
        else
            document.getElementById('msg_submit').disabled = true;
    };
});
