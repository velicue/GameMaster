(function() {
  var postJson, resSuccess;

  $('.login form').submit(function(e) {
    var callback, data, fields, i, len, v;
    e.preventDefault();
    e.stopPropagation();
    fields = $(this).find('input');
    data = {};
    for (i = 0, len = fields.length; i < len; i++) {
      v = fields[i];
      data[v.name] = v.value;
    }
    postJson(data, 'api/user/login', callback);
    return callback = function(res) {
      console.log(res);
      if (res.success === false) {
        return console.log('fuck failed');
      } else {
        return resSuccess();
      }
    };
  });

  $('.switch-signup').click(function(e) {
    $('.login').fadeOut();
    return $('.signup').fadeIn();
  });

  $('.switch-login').click(function(e) {
    $('.login').fadeIn();
    return $('.signup').fadeOut();
  });

  $('.signup input[name="email"]').focusout(function(e) {
    var callback, data;
    data = {};
    data[$(this).name] = $(this).value;
    postJson(data, '/api/user/repeat', callback);
    return callback = function(res) {
      console.log(res);
      if (res.repeat === true) {
        return $(this).attr("placeholder", "Repeated Email");
      }
    };
  });

  $('.signup form').submit(function(e) {
    var callback, data, fields, i, len, v;
    e.preventDefault();
    e.stopPropagation();
    fields = $(this).find('input');
    data = {};
    for (i = 0, len = fields.length; i < len; i++) {
      v = fields[i];
      data[v.name] = v.value;
    }
    postJson(data, 'api/user/register', callback);
    return callback = function(res) {
      console.log(res);
      if (res.success === false) {
        return console.log('fuck failed');
      } else {
        return resSuccess();
      }
    };
  });

  postJson = function(data, url, callbackFunc) {
    return $.ajax({
      type: 'POST',
      url: url,
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: callbackFunc
    });
  };

  resSuccess = function() {
    $('.login').hide();
    $('.signup').hide();
    return $('.succeed').fadeOut();
  };

  $().ready(function() {
    $('.succeed').hide();
    return $('.signup').hide();
  });

}).call(this);
