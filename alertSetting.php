<?php
class AlertSetting{
	public $notificationEnabled = False;
	public $endNotificationEnabled = False;
	public $notificationStartTime = "00";
	public $notificationEndTime = "00";
	public $notificationType ="Alert";
	function __construct($notificationEnabled,$endNotificationEnabled,$notificationStartTime,$notificationEndTime,$notificationType){
		$this->notificationEnabled = $notificationEnabled;
		$this->endNotificationEnabled = $endNotificationEnabled;
		$this->notificationStartTime = $notificationStartTime;
		$this->notificationEndTime = $notificationEndTime;
		$this->notificationType = $notificationType;		
	}
	
	function getNotificationEnabled(){
		if($this->notificationEnabled == 1){
			return "checked";
		}	
	}
	
	function getNotificationType($option){
		if($option==$this->notificationType){
			return "selected='selected'";
		}
	}
	
	function getEndNotificationEnabled(){
		if($this->endNotificationEnabled == 1){
                        return "checked";
                }
	}

	function getNotificationStartTime(){
                        return $this->notificationStartTime;
        }

	function getNotificationEndTime(){
                        return $this->notificationEndTime;
        }

}
?>
