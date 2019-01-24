 // Load the SDK asynchronously
 (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v3.2&appId=290505404870444';
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'))
  
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
    // This is called with the results from from FB.getLoginStatus().
    function statusChangeCallback(response) {
      // The response object is returned with a status field that lets the
      // app know the current login status of the person.
      // Full docs on the response object can be found in the documentation
      // for FB.getLoginStatus().
      if (response.status === 'connected') {
        // Logged into your app and Facebook.
        // testAPI();
        FB.api('/me', function(response) {
            document.getElementById("facebook_id").value=response["id"];
        });
      } else {
        // The person is not logged into your app or we are unable to tell.
        document.getElementById('facebook_error_email_signup').innerHTML = 'Ensure that you are' +
          'logged into facebook on this browser';
      }
    }
  
  