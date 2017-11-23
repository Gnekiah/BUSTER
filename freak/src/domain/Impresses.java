package domain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "impresses")
public class Impresses {
    @Id
    @GeneratedValue
    private int iId;
    
    @Column(length = 32)
    private String iName;
    
    private boolean iDeleted;
    
    private String iCreateTime;
    
    private String iModifyTime;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="uId")
    private Users user;

    public int getiId() {
        return iId;
    }

    public void setiId(int iId) {
        this.iId = iId;
    }

    public String getiName() {
        return iName;
    }

    public void setiName(String iName) {
        this.iName = iName;
    }

    public boolean isiDeleted() {
        return iDeleted;
    }

    public void setiDeleted(boolean iDeleted) {
        this.iDeleted = iDeleted;
    }

    public String getiCreateTime() {
        return iCreateTime;
    }

    public void setiCreateTime(String iCreateTime) {
        this.iCreateTime = iCreateTime;
    }

    public String getiModifyTime() {
        return iModifyTime;
    }

    public void setiModifyTime(String iModifyTime) {
        this.iModifyTime = iModifyTime;
    }

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }

}
