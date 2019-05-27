<?php

define('PAGEUP', "\xEE\x80\x8E");
define('PAGEDOWN', "\xEE\x80\x8F");
define('END', "\xEE\x80\x90");
define('HOME', "\xEE\x80\x91");
define('TAB', "\xEE\x80\x84");
define('SPACE', "\xEE\x80\x8D");
define('ESCAPE', "\xEE\x80\x8C");
define('SHIFT', "\xEE\x80\x88");
define('KEY_DOWN', "\xEE\x80\x95");
define('KEY_UP', "\xEE\x80\x93");
define('KEY_ENTER', "\xEE\x80\x87");
define('SPACE', "\xEE\x80\x8D");

class WebTest extends PHPUnit_Extensions_Selenium2TestCase
{
    private $clickHecho;
    private $action;
    private $actionType;

    public function setUp()
    {
        $this->setHost('selenium');
        $this->setPort(4444);
        $this->setBrowserUrl('https://auth2.bixpe.com/Account/Login');
        $this->setBrowser('firefox');
        $this->clickHecho = false;
        $this->actionType = ['start', 'stop', 'lunch', 'comeBackFromLunch'];
        $this->action = getenv('ACTION');
        $this->action = (in_array($this->action, $this->actionType))? $this->action: 'start';
    }

    public function testTitle()
    {
        try {
            $this->bixpeAction();
	} catch(Exception $e) {
            error_log($e->getMessage());
        }

    }


    public function bixpeAction() {
        $this->_open('https://auth2.bixpe.com/Account/Login');
        $cssUser = 'css=input#Username';
        sleep(5);
        if ($this->_isInPage($cssUser)) {
            $this->_click($cssUser);
            sleep(2);
            $username = getenv('USER');
            $this->keys($username);
        }
        $this->keys(TAB);
        sleep(2);

        $cssPw = 'css=input#Password';
        if ($this->_isInPage($cssPw)) {
            $this->_click($cssPw);
            sleep(2);
            $password = getenv('PASS');
            $this->keys($password);
        }
        $this->keys(KEY_ENTER);
        sleep(10);

        if (!$this->verifyAction()) {
            $this->clicksAction();
            if (!$this->verifyAction()) {
                $this->tele('No se ha hecho la acción ' . $this->action . ', has de darle tú');
                sleep(240);
            }
        }

        sleep(10);
        $this->_open('https://worktime.bixpe.com/Home/Logout');
        sleep(6);

    }

    private function verifyAction()
    {
        $this->_open('https://worktime.bixpe.com/');
        $cssToAction = '';
        switch($this->action) {
            case 'start':
                $cssToAction = 'css=.sl-item:nth-child(1) i.fa.fa-play.fa-2x.text-success';
                break;
            case 'stop':
                $cssToAction = 'css=.sl-item:nth-child(1) .fa.fa-stop.fa-2x.text-danger';
                break;
            case 'lunch':
                $cssToAction = 'css=.sl-item:nth-child(1) i.fa.fa-pause.fa-2x.text-warning';
                break;
            case 'comeBackFromLunch':
                $cssToAction = 'css=.sl-item:nth-child(1) i.fa.fa-refresh.fa-2x.text-success';
                break;
        }

        sleep(5);
        if ($this->_isInPage($cssToAction)) {
            $this->tele('Está ' . $this->action . ' OK no hago nada');
            sleep(5);
            return true;
        }
        else {
            sleep(5);
            return false;
        }
    }

    public function tele($message) {
	try {
            $botToken = getenv('BOT_TOKEN_TELEGRAM');
            $website = "https://api.telegram.org/".$botToken."/sendMessage";
            $chatId = getenv('CHAT_ID_TELEGRAM');
            $params = [
                'chat_id'=>$chatId,
                'text'=>$message,
            ];
            $ch = curl_init($website);
            curl_setopt($ch, CURLOPT_HEADER, false);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, ($params));
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            $result = curl_exec($ch);
            curl_close($ch);
            error_log($result);
	    } catch(Exception $e) {
                error_log($e->getMessage());
        }
        
    }

    private function clicksAction()
    {
        $cssToAction = '';

        switch($this->action) {
            case 'start':
                $cssToAction = 'css=button#btn-start-workday';
                break;
            case 'stop':
                $cssToAction = 'css=button#btn-stop-workday';
                break;
            case 'lunch':
                $cssToAction = 'css=button#btn-pause-lunch';
                break;
            case 'comeBackFromLunch':
                $cssToAction = 'css=button#btn-resume-workday';
                break;
        }

        if ($this->_isInPage($cssToAction)) {
            $this->_click($cssToAction);
            sleep(4);
        }

        sleep(10);
        if ($this->action == 'start' || $this->action == 'stop') {
            $cssToAction = 'css=button.swal2-confirm.swal2-styled';
            if ($this->_isInPage($cssToAction)) {
                $this->_click($cssToAction);
                sleep(10);
            }
        }

    }

    public function _open($url) {
        $this->url($url);
    }

    public function _isInPage($xpa) {
        $element='';

        try {
            if (preg_match('/xpath/', $xpa)) {
                $element = $this->byXPath(str_replace("xpath=", "", $xpa));
                if(is_null($element) || !$element) {
                    return false;
                }
                return true;
            } else if (preg_match('/css/', $xpa)) {
                $element = $this->byCssSelector(str_replace("css=", "", $xpa));
                if(is_null($element) || !$element) {
                    return false;
                }
                return true;
            } else if (preg_match('/id/', $xpa)) {
                $element = $this->byId(str_replace("id=", "", $xpa));
                if(is_null($element) || !$element) {
                    return false;
                }
                return true;
            } else if (preg_match('/name/', $xpa)) {
                $element = $this->byName(str_replace("name=", "", $xpa));
                if(is_null($element) || !$element) {
                    return false;
                }
                return true;
            }
        }
        catch(Exception $e) {
            error_log('No encuentro en source: '. $xpa);
            return false;
        }

    }

    function _click($locator) {
        $clikSuccessfully = true;
        try {
            $iterations = 0;
            do {
                $iterations++;
                $this->keys(TAB);
                sleep(0.5);
                try {
                    if(preg_match('/xpath/',$locator)){
                        $locatorCleaned = str_replace('xpath=','',$locator);
                        $element = $this->byXPath( $locatorCleaned);
                        $element->click();
                        $clikSuccessfully = true;
                    }
                    else if(preg_match('/css/',$locator)){
                        $locatorCleaned = str_replace('css=','',$locator);
                        $element = $this->byCssSelector($locatorCleaned);
                        $element->click();
                        $clikSuccessfully = true;
                    }
                    else if(preg_match('/id/',$locator)){
                        $locatorCleaned = str_replace('id=','',$locator);
                        $element = $this->byId($locatorCleaned);
                        $element->click();
                        $clikSuccessfully = true;
                    }
                    else if(preg_match('/name/',$locator)){
                        $locatorCleaned = str_replace('name=','',$locator);
                        $element = $this->byName($locatorCleaned);
                        $element->click();
                        $clikSuccessfully = true;
                    }
                    else {
                        error_log('tenemos un problema no sabemos que tipo de locator es');
                    }
                    sleep(2);
                }catch(Exception $e) {
                    if($clikSuccessfully) {
                        $this->keys(HOME);
                        sleep(3);
                    }
                    $clikSuccessfully = false;
                    error_log('salgo excepcion de click');
                }
                if($clikSuccessfully){error_log('$clikSuccessfully es true');}
                else {error_log('$clikSuccessfully es false');}

            }while(!$clikSuccessfully && $iterations < 1);
        }
        catch(Exception $e){
            error_log($e->getMessage());
        }
    }

}


