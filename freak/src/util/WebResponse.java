package util;

import java.util.HashMap;

public class WebResponse extends HashMap<String, Object> {
	private static final long serialVersionUID = 1L;
	public WebResponse() {
		this.setSuccess(true);
	}

	public void setSuccess(boolean success) {
		this.put("success", success);
	}
	
	public void setMsg(String msg) {
		this.put("msg", msg);
	}

	public void setCode(String code) {
		this.put("code", code);
	}
}
