package monolith.spring.dao;

import java.util.List;

import monolith.spring.model.HotelSpecial;

public interface HotelSpecialDAO {

	public List<HotelSpecial> findAll();
	public HotelSpecial findById(int id);
}
