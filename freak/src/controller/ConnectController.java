package controller;

import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import domain.Connects;
import domain.Messages;
import domain.Users;
import util.WebResponse;

@RestController
@Transactional
public class ConnectController extends HibernateController {

    @RequestMapping(value="/connect.do")
    public WebResponse upload(String title, String text) {
        WebResponse response=new WebResponse();
        
        Connects connect = new Connects();
        Messages message = new Messages();
        Users user1 = new Users();
        Users user2 = new Users();
        
        user1.setuId(1);
        user2.setuId(2);
        this.save(user1);
        this.save(user2);
        
        connect.setUser1(user1);
        connect.setUser2(user2);
        this.save(connect);
        
        message.setUser(user1);
        message.setmCreateTime(Long.toString(System.currentTimeMillis()));
        message.setConnect(connect);
        this.save(message);
        
        return response;
    }
}
