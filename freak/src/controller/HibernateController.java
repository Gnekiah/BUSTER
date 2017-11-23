package controller;
import java.io.Serializable;

import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;

public class HibernateController extends BaseController {
	@Autowired
	private SessionFactory sessionFactory;
	protected Session getSession() {
        return sessionFactory.getCurrentSession();
    }
	protected Query createQuery(String queryString)
	{
		return this.getSession().createQuery(queryString);
	}
	@SuppressWarnings("unchecked")
	protected <T> T get(Class<T> clazz,Serializable id)
	{
		
		return (T) this.getSession().get(clazz, id);
	}
	protected void save(Object entity)
	{
		this.getSession().save(entity);
	}
	protected void delete(Object entity)
	{
		this.getSession().delete(entity);
	}
	protected void update(Object entity)
	{
		this.getSession().update(entity);
	}
}
