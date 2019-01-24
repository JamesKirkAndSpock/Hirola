 // Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v3.2&appId=290505404870444&autoLogAppEvents=1';
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

window.fbAsyncInit = function() {
  FB.init({
    appId      : '290505404870444',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
};
  function statusChangeCallback(response) {
    if (response.status === 'connected') {
      document.getElementById('status').innerHTML = 'You are currently ' +
      'logged into facebook. Log out to signup as a different user.';
    } else {
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
  }
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
      target = "/me?fields=email,id,first_name,last_name&access_token=" + response["authResponse"]["accessToken"];
      handleDataInput(target);
    });
  }

  function handleDataInput(target) {
    FB.api(target, function(response){
      document.getElementById("facebook_email").value=response["email"];
      document.getElementById("facebook_id").value=response["id"];
      document.getElementById("facebook_first_name").value=response["first_name"];
      document.getElementById("facebook_last_name").value=response["last_name"];
      document.getElementById("facebook_form").submit()
     });
  }
