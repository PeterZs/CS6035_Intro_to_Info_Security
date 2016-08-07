<?php

// this file handles database interaction

class Database {
    var $database;
    function Database($filename){
        $this->database = new SQLite3($filename);
        $this->database->busyTimeout(500);
        $this->database->exec('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, eid TEXT, password TEXT, salt TEXT, accounting TEXT)');
    }
    function query($q){
        $result = $this->database->query($q);
        return new ResultSet($result);
    }

    function escape($s){
        return $this->database->escapeString($s);
    }

    function __destruct() {
        $this->database->close();
    }
}

class ResultSet {
    var $result;
    var $currentRow;
    
    function ResultSet(&$result){
        $this->result =& $result;
    }

    function getCurrentValueByName($name){
        if($this->currentRow)
            return $this->currentRow[$name];
        return false;
    }

    function next(){
        $this->currentRow = $this->result->fetchArray();
        return $this->currentRow;
    }
    
    // ignore row number this is so broke
    function getValueByNr($rowno,$colno){
        if(!$this->currentRow)
            $this->next();
        return $this->currentRow[$colno];

    }

    function getCurrentValues(){
        if(!$this->currentRow)
            $this->next();
        return $this->currentRow;
    }

}
?>
