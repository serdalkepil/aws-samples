package monolith.spring.service;

import java.util.List;

import monolith.spring.model.FlightSpecial;

public interface FlightSpecialService {

	public List<FlightSpecial> findAll();
	public FlightSpecial findById(int id);
	
}
