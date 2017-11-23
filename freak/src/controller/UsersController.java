package controller;

import java.io.IOException;

import javax.servlet.http.HttpServletResponse;

import org.hibernate.Query;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import domain.Users;
import util.WebResponse;

@RestController
@Transactional
public class UsersController extends HibernateController {
    
    @RequestMapping(value="/login.do")
    public WebResponse login(String username, String password, HttpServletResponse req) {
        WebResponse response=new WebResponse();
        Query q=this.createQuery("select uId from Users where uName=?");
        q.setParameter(0, username);
        //q.setParameter(1, password);
        
        if ((int)q.list().size() != 0) {
            try { req.sendRedirect("home.html"); } catch (IOException e) { e.printStackTrace(); }
        }
        else {
            try { req.sendRedirect("500.html"); } catch (IOException e) { e.printStackTrace(); }
        }
        return response;
    }
    
    @RequestMapping(value="/register.do")
    public WebResponse register(String username, String password, HttpServletResponse req) {
        WebResponse response=new WebResponse();
        
        Users user=new Users();
        user.setuName(username);
        user.setuPasswd(password);
        this.save(user);
        
        try { req.sendRedirect("home.html"); } catch (IOException e) { e.printStackTrace(); }
        return response;
    }
}
