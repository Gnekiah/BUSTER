package controller;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;
import org.springframework.web.bind.annotation.ExceptionHandler;

import com.fasterxml.jackson.databind.ObjectMapper;

import util.WebResponse;

public class BaseController {
	protected Logger logger = Logger.getLogger(BaseController.class);
	@ExceptionHandler
	public void exHandler(HttpServletResponse response,Exception ex)
	{
		logger.error(ex.getMessage(),ex);
		WebResponse webResponse=new WebResponse();
		webResponse.setSuccess(false);
		webResponse.setMsg(ex.getMessage());
		try {
			PrintWriter writer=response.getWriter();
			ObjectMapper mapper=new ObjectMapper();
			writer.println(mapper.writeValueAsString(webResponse));
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
}
