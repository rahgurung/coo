var global_channel_list = [];
var global_user_list = [];
var global_current_channel;
var msgType = "PUBLIC";
let displayname = localStorage.getItem('displayname');;


// this function weighs and unweighs the channel
// chn means channel parameter here
function clickhandler(chn) {
  if (global_channel_list.includes(global_current_channel)) {
    document.getElementbyId(global_current_channel).style.fontWeight = "normal";
  }

  global_current_channel = chn;
  msgType = "PUBLIC";
  let header = document.getElementbyId("message_header");

  document.getElementbyId(global_current_channel).style.fontWeight = "bold";
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

  hdr.innerHTML = "Conversations with " + usr;
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
