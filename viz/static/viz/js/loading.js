(function (d) {
  d.getElementById('form').onsubmit = function () {
    d.getElementById('submit').style.display = 'none';
    d.getElementById('loading2').style.display = 'block';
  };
}(document));