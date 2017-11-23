package domain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "extends")
public class Extends {
    @Id
    @GeneratedValue
    private int eId;
    
    @Column(length = 8)
    private String eType;
    
    @Column(length = 32)
    private String eSource;
    
    @ManyToOne(optional=false)
    @JoinColumn(name="iId")
    private Impresses impress;

    public int geteId() {
        return eId;
    }

    public void seteId(int eId) {
        this.eId = eId;
    }

    public String geteType() {
        return eType;
    }

    public void seteType(String eType) {
        this.eType = eType;
    }

    public String geteSource() {
        return eSource;
    }

    public void seteSource(String eSource) {
        this.eSource = eSource;
    }

    public Impresses getImpress() {
        return impress;
    }

    public void setImpress(Impresses impress) {
        this.impress = impress;
    }
    
    
}
