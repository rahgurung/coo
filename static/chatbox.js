var global_channel_list = [];
var global_user_list = [];
var global_current_channel;
var msgType = "PUBLIC";
let displayname = localStorage.getItem('displayname');


// this function weighs and unweighs the channel
// chn means channel parameter here
function clickhandler(chn) {
  if (global_channel_list.includes(global_current_channel)) {
    document.getElementById(global_current_channel).style.fontWeight = "normal";
  }

  global_current_channel = chn;
  msgType = "PUBLIC";
  let header = document.getElementById("message_header");

  document.getElementById(global_current_channel).style.fontWeight = "bold";
  header.innerHTML = " Messages on " + global_current_channel + "channel";
  localStorage.setItem("channel", global_current_channel)
  configure_msgs(global_current_channel, msgType)
}


// this function weighs the new channel and unweighs the old channel
// chn means channel parameter here
function dm_clickhandler(usr) {
  let header = document.getElementById("message_header");
  msgType = "PRIVATE";

  document.getElementById(global_current_channel).style.fontWeight = "normal";

  global_current_channel = usr;
  document.getElementById(usr).style.fontWeight = "bold";

  header.innerHTML = "Conversations with " + usr;
  configure_msgs(usr, msgType);
}


// this function adds the channel and creates new row with
// the name of new channel, -1 in inserCell insert new channel_list
// in the end whereas 0 does it in the beginning
function add_channel(chn, selected) {
  const new_chn_row = document.createElement('TR');
  var c = new_chn_row.insertCell(-1);

  c.innerHTML = chn;
  c.setAttribute("id", chn);
  c.setAttribute("class", "channel-listing");
  c.setAttribute("data-channel", chn);

  let chntrow = chn + "row"
  new_chn_row.setAttribute("id", chntrow);
  new_chn_row.setAttribute("class", "channel-listing");
  new_chn_row.setAttribute("data-channel", chn);
  global_channel_list.push(chn);

  var emnt = new_chn_row.querySelector("td");
  emnt.addEventListener("click", function() { clickhandler (chn); });
  document.getElementById('hoverTable').append(new_chn_row);
  if (selected == 1) {
    clickhandler(chn);
  }
}

// this function activates a user
function activate_user(usr) {
  const logged_in = document.getElementById(usr);
  console.log ("AU: usr = ", usr);
  logged_in.style.fontWeight = "normal";
}

// this function deactivates the users
function deactivate_user(usr) {
  const logged_in = document.getElementById(usr);
  console.log("DU: logged in is ", logged_in);
  logged_in.style.fontWeight = "normal";
  logged_in.style.fontStyle = "italic";
}

// this function adds user to the chatbox
function add_user(usr) {
  const new_usr_row = document.createElement('TR');
  var c = new_usr_row.insertCell(-1);

  c.innerHTML = usr;
  c.setAttribute("id", usr);
  c.setAttribute("class", "user-listing");
  c.setAttribute("data-user", usr);

  let usrtrow = usr + "row"
  new_usr_row.setAttribute("id", usrtrow);
  new_usr_row.setAttribute("class", "user-listing");
  new_usr_row.setAttribute("data-user", usr);
  global_user_list.push(usr);

  var emnt = new_usr_row.querySelector("td");
  emnt.addEventListener("click", function() { dm_clickhandler (usr); });
  document.getElementById('user_list').append(new_usr_row);
}

// this fucntion configures the channel by using AJAX request
// to get the list of channel and setting the global_current_channel
// Extract list of channels and populate variable and dropdown menu
function configure_channels() {
  console.log("configuring channels");
  const request = new XMLHttpRequest();
  request.open('POST', '/query_channels');

  if (localStorage.getItem('channel')) {
    global_current_channel = localStorage.getItem('channel');
  }
  else {
    global_current_channel = "General";
  }

  request.onload = () => {
    const data = JSON.parse(request.responseText);

  	if (data.success) {
	     var channels = data["channel_list"];
	     for (var i = 0, len = channels.length; i < len; i++) {
		       if (channels[i] == global_current_channel) {
		           add_channel(channels[i], 1);
           }
		       else {
		           add_channel(channels[i], 0);
		       }
	     }
     }
     else {
       console.log("API call failed !")
     }

// this fucntion adds a message to the displayed message list
function add_message(msg) {
    const new_row = document.createElement('TR');
    var c = new_row.insertCell(0);

    let ts = "<font class='tstamp'>" + msg["timestamp"] + "</font>";
    let dn = " <font class='dname'> @" + msg["user_from"] + "</font><br>";

    let n_msg = ts + dn + msg["msg_txt"];
    c.innerHTML = n_msg;
    document.getElementById('message_list').append(new_row);
}
  }

  request.send();
}

// this function clears messages when switching channels
function clear_messages() {
    var myNode = document.getElementById('message_list');

    while (myNode.firstChild) {
	     myNode.removeChild(myNode.firstChild);
    }
}


// this function clears user list
function clear_users() {
    var myNode = document.getElementById('user_list');

    while (myNode.firstChild) {
	myNode.removeChild(myNode.firstChild);
    }
}

// this function configure messages by making a AJAX request and then
// adding messages using add_message
// add data to send with request for messages on this channel

function configure_msgs(chn, isPub) {
  clear_messages();
  const request = new XMLHttpRequest();
  request.open('POST', '/query_messages');

  console.log("CM: msgType = ", msgType);

  request.onload = () => {
    const data = JSON.parse(request.responseText);

    if(data.success) {
      console.log ("configure_msgs: success. messages =", data["channel_msgs"]);
      var messages = data["channel_msgs"];
      for (var i = 0, len = messages.length; i < len; i++) {
        add_message(messages[i]);
      }
    }
  }

  const data = new FormData();
  data.append('channel', chn);
  data.append('displayname', displayname);
  data.append('msg_type', msgType);

  console.log ("CM: data = ", data)

  request.send(data);
  return false;
}

// this configures the users of channels, extracts
// dictionary of messages and populate message pane
function configure_usrs() {
  clear_users();

  const request = new XMLHttpRequest();
  request.open('POST', '/query_users');
  request.onload = () => {
	   const data = JSON.parse(request.responseText);

	   if (data.success) {
	      users = data["active_users"]
	      for (var i = 0, len = users.length; i < len; i++) {
		        if (users[i] != 'None') {
		        console.log ("configure:users: adding ", users[i]);
		        add_user(users[i]);
		        }
	      }
	   }
	   else {
	   console.log("API query users failed");
     }
  }
  request.send();
  return false;
}

// socketio logic is here, which configures the submit buttons
// add new announced channel to channel listing
// when a new mesage is announced , adds to message list
// and submits channel, timestamp, user_from, msg_txt
document.addEventListener('DOMContentLoaded', () => {

  console.log("hey dom content is just loaded !");
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  let dn = document.getElementById("dname").innerHTML;

  if (dn != displayname) {
    displayname = dn;
    localStorage.setItem("displayname", dn);
  }

  socket.on('connect', () => {
    console.log("socket io connected");
    var id = socket.io.engine.id;
    socket.emit("join", {"displayname": displayname, "room": id});
    configure_channels();
    configure_usrs();
  });

  document.getElementById('submit').disabled = true;
  document.getElementById('msg_submit').disabled = true;

  document.getElementById('channel_name').onkeyup = () => {
    if (document.getElementById('channel_name').value.length > 0)
    document.getElementById('submit').disabled = false;
    else
      document.getElementById('submit').disabled = true;
  };

  document.getElementById('message_text').onkeyup = () => {
  if (document.getElementById('message_text').value.length > 0)
    document.getElementById('msg_submit').disabled = false;
  else
    document.getElementById('msg_submit').disabled = true;
  };

  document.getElementById("new_channel").onsubmit = () => {
    var chn = document.getElementById('channel_name').value;
    if(global_channel_list.includes(chn)) {
      alert ("Channel Already Exists");
    }
    else {
      document.getElementById('channel_name').value = "";
      document.getElementById('submit').disabled = true;
      socket.emit('submit channel', {'channel': chn});
    }
    return false;
  };

  socket.on('announce channel', data => {
    add_channel(data["channel"], 0);
  });

  socket.on('new user', data => {
    if ((data["username"] == displayname) || (global_user_list.includes(data["username"]))) {
      return false;
    }
    else {
      add_user(data["username"]);
    }
  });

  socket.on( 'announce message', data => {
    console.log ("AM: arrived. channel = ", data["channel"]);
    if (data["channel"] == global_current_channel) {
      console.log("announce message: msgType = ", data["msg_type"], "channel = ", data["channel"]);
  		add_message(data);
    }
  });

  document.getElementById("new_message").onsubmit = () => {
    var val = document.getElementById('message_text').value;
    var dt = new Date();
    var dn = document.getElementById('displayname').value;

    document.getElementById('message_text').value = "";
    document.getElementById('msg_submit').disabled = true;
    chn = global_current_channel;

    socket.emit('submit message', {'msg_txt': val, 'channel': chn, 'timestamp': dt, 'user_from': displayname});
    return false;
  };

});
