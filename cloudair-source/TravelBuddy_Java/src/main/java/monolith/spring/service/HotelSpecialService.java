package monolith.spring.service;

import java.util.List;

import monolith.spring.model.HotelSpecial;

public interface HotelSpecialService {

	public List<HotelSpecial> findAll();
	public HotelSpecial findById(int id);
	
}
