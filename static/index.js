document.addEventListener('DOMContentLoaded', () => {

    // by default submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#id1').onkeyup = () => {
        var my_string = document.querySelector('#id1').value;
        var spaceCount = (my_string.split(" ").length - 1);
        if (document.querySelector('#id1').value.length != spaceCount)
            document.querySelector('#submit').disabled = false;
        else
            document.querySelector('#submit').disabled = true;
    };
});
