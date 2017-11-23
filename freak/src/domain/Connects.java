package domain;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "connects")
public class Connects {
    @Id
    @GeneratedValue
    private int cId;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="uId1")
    private Users user1;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="uId2")
    private Users user2;

    public int getcId() {
        return cId;
    }

    public void setcId(int cId) {
        this.cId = cId;
    }

    public Users getUser1() {
        return user1;
    }

    public void setUser1(Users user1) {
        this.user1 = user1;
    }

    public Users getUser2() {
        return user2;
    }

    public void setUser2(Users user2) {
        this.user2 = user2;
    }

}
