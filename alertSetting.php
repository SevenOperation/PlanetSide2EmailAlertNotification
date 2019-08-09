<?php
class AlertSetting{
	private $notificationEnabled = False;
	private $endNotification = False;
	private $notificationStartHour = "00";
	private $notificationEndHour = "00";
	private $alertNotificationOnly ="Alert";
	private $indarNotification = False;
	private $amerishNotification = False;
	private $esamirNotification = False;
	private $hossinNotification = False;
	
	function __construct($notificationEnabled,$endNotificationEnabled,$notificationStartTime,$notificationEndTime,$notificationType,$indarNotification,$amerishNotification,$esamirNotification,$hossinNotification){
		$this->notificationEnabled = $notificationEnabled;
		$this->endNotification = $endNotificationEnabled;
		$this->notificationStartHour = $notificationStartTime;
		$this->notificationEndHour = $notificationEndTime;
		$this->alertNotificationOnly = $notificationType;	
		$this->indarNotification = $indarNotification;	
		$this->amerishNotification = $amerishNotification;	
		$this->esamirNotification = $esamirNotification;	
		$this->hossinNotification = $hossinNotification;	
			
	}
	
	function setNotificationEnabled($state){
		$this->notificationEnabled = $state;
	}

	function convertNotificationEnabled(){
		if($this->notificationEnabled == 1){
			return "checked";
		}	
	}

	function getNotificationEnabled(){
		return $this->notificationEnabled;
	}

	function setAlertNotificationOnly($state){
		$this->alertNotificationOnly = $state;
	}
	
	function convertAlertNotificationOnly($option){
		if($option==$this->alertNotificationOnly){
			return "selected='selected'";
		}
	}
	
	function getAlertNotificationOnly(){
		return $this->alertNotificationOnly;
	}
	



	//EndNotification
	function setEndNotification($state){
		$this->endNotification = $state;
	}

	function convertEndNotification(){
		if($this->endNotification == 1){
                        return "checked";
                }
	}

	function getEndNotification(){
		return $this->endNotification;
	}
	


	//StartHour
	function setNotificationStartHour($hour){
		$this->notificationStartHour = $hour;
	}

	function getNotificationStartHour(){
                return $this->notificationStartHour;
        }
	


	//EndHour
	function setNotificationEndHour($hour){
		$this->notificationEndHour = $hour;
	}

	function getNotificationEndHour(){
                return $this->notificationEndHour;
        }



	//Indar
	function setIndarNotification($state){
		$this->indarNotification = $state;
	}
		
	private function convertIndarNotification(){
		if($this->indarNotification == 1){
                        return "checked";
                }
	}

	function getIndarNotification(){
			return $this->indarNotification;
	}



	//Amerish
	function setAmerishNotification($state){
		$this->amerishNotification = $state;
	}
	
	private function convertAmerishNotification(){
		if($this->amerishNotification == 1){
			return "checked";
		}
	}
	
	function getAmerishNotification(){
		return $this->amerishNotification;
	}



	//Esamir
	function setEsamirNotification($state){
		$this->esamirNotification = $state;
	}
	
	private function convertEsamirNotification(){
		if($this->esamirNotification == 1){
                        return "checked";
	        }
	}

	function getEsamirNotification(){
		return $this->esamirNotification;
	}



	//Hossin
	function setHossinNotification($state){
		$this->hossinNotification = $state;
	}
	
	private function convertHossinNotification(){
		if($this->hossinNotification == 1){
                        return "checked";                                                                                               
		}
	}

	function getHossinNotification(){
		return $this->hossinNotification;
	}


	function getAlertSettingUI(){
		$ui = "<form action='updateAlertSetting' method='POST'>\n";
		$ui .= "<p> Planetside 2 Alert Settings:</p>\n";
		$ui .= "<p> Enable PS2 Alert notification.<input type='checkbox' name='ps2NotificationState' {$this->convertNotificationEnabled()} /></p>";
		$ui .= "<p> Send email when an <select name='eventTypes'>";
		$ui .= "<option value='0' title='You will get notified by every game event' {$this->convertAlertNotificationOnly(0)}>Event</option>";
		$ui .= "<option value='1' title='You will only get notified when an game alert event is happening '{$this->convertAlertNotificationOnly(1)}>Alert</option>";
		$ui .= "</select>";
		$ui .= " is happening.</p>";
		$ui .= "<p> Only notify when and Event/Alert is happening on Indar<input type='checkbox' name='indar' {$this->convertIndarNotification()} />";
		$ui .= "Amerish<input type='checkbox' name='amerish' {$this->convertAmerishNotification()} />";
		$ui .= "Esamir<input type='checkbox' name='esamir' {$this->convertEsamirNotification()} />";
		$ui .= "Hossin<input type='checkbox' name='hossin' {$this->convertHossinNotification()} /></p>";
		$ui .= "<p> Only send those between <input type='number' max='24' id='from' name='from' value='{$this->getNotificationStartHour()}'required/> and <input max='24' type='number' id='until' name='until' value='{$this->getNotificationEndHour()}' required/> o'clock. (24h format) </p>";
		$ui .= "<p> Also send an Event/Alert end notification.<input title='If checked you also get a notification when an Event/Alert ended' type='checkbox' name='ps2EndEventNotification' {$this->convertEndNotification()}/></p>";
		$ui .= "<p><button>Submit PS2 Alert settings</button></p>";
		$ui .= "</form>";
		return $ui;
	}

}
?>
