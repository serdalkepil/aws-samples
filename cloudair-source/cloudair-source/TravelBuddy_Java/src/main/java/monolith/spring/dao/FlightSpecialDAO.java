package monolith.spring.dao;

import java.util.List;

import monolith.spring.model.FlightSpecial;

public interface FlightSpecialDAO {

	public List<FlightSpecial> findAll();
	public FlightSpecial findById(int id);
}
