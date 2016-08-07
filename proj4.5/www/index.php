<?php
// initialize global variables, authentication and database connections
include('includes/common.php');

// if the login or registration form has been submitted, handle it
$action = @$_POST['action'];
if ($action == 'login') {
	$auth->login($_POST['login'], $_POST['pw']);
} elseif ($action == 'register') {
	$auth->register($_POST['name'], $_POST['login'], $_POST['pw1'], $_POST['pw2']);
}

// if the user is logged in, redirect him to home.php
if ($auth->user_id()) {
	header('location: /account.php');
}


// otherwise, display a login page
include('includes/header.php');
?>
   <div class="row">
    <div class="span4 offset1">
     <form method="post">
      <fieldset>
       <legend>Please log in</legend>
       <label>account ID:</label>
       <input type="hidden" name="secret" value="whatdoido?">
       <input type="text" name="login" value="<?php filter_var($_POST['login'], FILTER_SANITIZE_STRING) ?>">
       <label>Password:</label>
       <input type="password" name="pw" value="<?php filter_var($_POST['pw'], FILTER_SANITIZE_STRING) ?>">
       <div>
        <button class="btn" type="submit" name="action" value="login">Log In</button>
       </div>
      </fieldset>
     </form>
    </div>
    <div class="span4 offset1 register">
     <form method="post">
      <fieldset>
       <legend>First time? Register here:</legend>
       <label>Name:</label>
       <input type="text" name="name" value="<?php filter_var($_POST['name'], FILTER_SANITIZE_STRING) ?>">
       <label>account ID:</label>
       <input type="text" name="login" value="<?php filter_var($_POST['login'], FILTER_SANITIZE_STRING) ?>">
       <label>Password</label>
       <input type="password" name="pw1" value="<?php filter_var($_POST['pw1'], FILTER_SANITIZE_STRING) ?>">
       <label>Repeat password</label>
       <input type="password" name="pw2" value="<?php filter_var($_POST['pw2'], FILTER_SANITIZE_STRING) ?>">
       <div>
        <button class="btn" type="submit" name="action" value="register">Register</button>
       </div>
      </fieldset>
     </form>
    </div>
   </div>
<?php
include('includes/footer.php');
?>
