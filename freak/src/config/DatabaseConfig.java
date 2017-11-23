package config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jndi.JndiObjectFactoryBean;

@Configuration
public class DatabaseConfig {
	@Bean
	public JndiObjectFactoryBean dataSource(){
		JndiObjectFactoryBean bean=new JndiObjectFactoryBean();
		bean.setJndiName("java:comp/env/jdbc/freak");
		return bean;
	}

	
}
