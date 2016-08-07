<?php
// initialize global variables, authentication and database connections
include('includes/common.php');

// if the user is NOT logged in, redirect him to login page
if (!$auth->user_id()) {
	header('location: /');
}


// initiate csrf prevention
$_SESSION['csrf_token'] = mt_rand();

// handle the form submission
$action = @$_POST['action'];
if ($action == 'save') {
	// verify CSRF protection
	$expected = mt_rand();
	$teststr = $_POST['account'].$_POST['challenge'].$_POST['routing'];
	for ($i = 0; $i < strlen($teststr); $i++) {
		$expected = (13337 * $expected + ord($teststr[$i])) % 100000;
	}
	if ($_POST['response'] != $expected) {
		notify('CSRF attempt prevented!'.$teststr.'--'.$_POST['response'].' != '.$expected, -1);
	} else {
		$accounting = ($_POST['account']).':'.($_POST['routing']);
		$db->query("UPDATE users SET accounting='$accounting' WHERE user_id='".$auth->user_id()."'");
		notify('Changes saved');
	}
}

$eid = @$_GET['eid'];
if ($eid) {
	$name = $db->query("SELECT name FROM users WHERE eid='$eid'")->next();	
}

// grab form values from database if available
$accounting = $db->query("SELECT accounting FROM users WHERE user_id='".$auth->user_id()."'")->next();
$values = explode(':', $accounting['accounting']);
$account = @$values[0];
$routing = @$values[1];

include('includes/header.php');
?>
    <div class="row">
     <div class="span4 offset1">
      <h3>Payment information</h3>
      <p>Your paycheck will be deposited in the following bank account on the 1nd of each month.</p>
      <form method="post" action="/account.php">
       <label>Account number:</label>
       <input id="account" type="number" name="account" value="<?php echo $account ?>">
       <label>Routing number:</label>
       <input id="route" type="number" name="routing" value="<?php echo $routing ?>">
       <input id="csrfc" type="hidden" name="challenge" value="<?php echo $_SESSION['csrf_token'] ?>">
       <input id="csrfr" type="hidden" name="response" value="">
       <div>
        <button class="btn submit" name="action" value="save">Save</button>
       </div>
      </form>
     </div>
     <script>

// fairly trivial string hashing function
String.prototype.hashCode = function(){
  var hash = 1;
  for (i = 0; i < this.length; i++) {
    hash = (13337*hash + this.charCodeAt(i)) % 100000;
  }
  return hash;
}

var a = document.getElementById('account');
var r = document.getElementById('route');
function change() {
	var challenge = document.getElementById('csrfc').value;
	document.getElementById('csrfr').value = (a.value+challenge+r.value).hashCode()
}
a.onkeyup = change;
r.onkeyup = change;
change();
     </script>
     <div class="span4 offset2">
      <h3>Look up name</h3>
      <p>You may use this form to look up a user's name using their account ID</p>
      <form method="get">
       <label>account ID:</label>
       <input type="text" name="eid" value="<?php echo stripslashes(@$eid) ?>">
       <div>
        <button class="btn submit">Look up</button>
       </div>
      </form>
<?php if (@$eid): ?>
      <hr>
<?php	if ($name): ?>
      <div id="eid-entry">
      <!-- user data appears here -->
      </div>
      <div id="result-data" data-result="name='<?php echo $name['name'] ?>'">
      <script>
eval(document.getElementById('result-data').getAttribute('data-result'));
document.getElementById('eid-entry').innerHTML = "<div><?php echo $eid ?> registered as:\n"+name+"</div>";
      </script>
<?php	else: ?>
      <p>This account ID is not registered.</p>
<?php 	endif; ?>
<?php endif; ?>
     </div>
<?php
include('includes/footer.php');
?>
