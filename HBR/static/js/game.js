var last_move = ""

var url = window.location.href;
if (url.charAt(url.length - 1) == '/') {
  url = url.substring(0, url.length - 1);
}

/* Game ID */
const game_id = url.substring(url.lastIndexOf('/') + 1, url.length);

var get_move = function () {
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var move = this.responseText;
      last_move = move;
      update_state(move);
      setTimeout(function () {
        get_move();
      }, 1000)
    }
  };

  var fd = new FormData();
  fd.append('last_move', last_move);

  xhttp.open('POST', '/get_move/' + game_id);
  xhttp.send(fd);
}

var guess = function (opponent) {
  var letter = $("#" + opponent + "-guess").val();
}

var update_state = function (move) {
  console.log('bees!')
}

var limit = function (id) {
  const r = RegExp("[A-Za-z]");
  var v = document.getElementById(id);

  if (v.value.length == 1) {
    if (!r.test(v.value)) {
      v.value = "";
    };
  }
  if (v.value.length == 2) {
    if (!r.test(v.value.substring(1, 2))) {
      v.value = v.value.substring(0, 1);
    }
  }

  if (v.value.length > 1) {
    v.value = v.value.substring(1, 2);
  };
  v.value = v.value.toUpperCase()
};
