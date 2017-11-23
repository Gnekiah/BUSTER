package controller;

import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import domain.Extends;
import domain.Impresses;
import domain.Users;
import util.WebResponse;

@RestController
@Transactional
public class UploadController extends HibernateController {

    @RequestMapping(value="/upload.do")
    public WebResponse upload(String title, String text) {
        WebResponse response=new WebResponse();
        
        Users user = new Users();
        user.setuId(1);
        
        Impresses impress=new Impresses();
        impress.setiName(title);
        impress.setiDeleted(false);
        impress.setiCreateTime(Long.toString(System.currentTimeMillis()));
        impress.setiModifyTime(Long.toString(System.currentTimeMillis()));
        impress.setUser(user);
        this.save(impress);
        
        Extends extend = new Extends();
        extend.seteSource(title);
        extend.seteType("text");
        extend.setImpress(impress);
        this.save(extend);
        
        return response;
    }
}
