package domain;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "messages")
public class Messages {
    @Id
    @GeneratedValue
    private int mId;
    
    private String mCreateTime;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="uId")
    private Users user;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="cId")
    private Connects connect;

    public int getmId() {
        return mId;
    }

    public void setmId(int mId) {
        this.mId = mId;
    }

    public String getmCreateTime() {
        return mCreateTime;
    }

    public void setmCreateTime(String mCreateTime) {
        this.mCreateTime = mCreateTime;
    }

    public Users getUser() {
        return user;
    }

    public void setUser(Users user) {
        this.user = user;
    }

    public Connects getConnect() {
        return connect;
    }

    public void setConnect(Connects connect) {
        this.connect = connect;
    }
    
    
}
