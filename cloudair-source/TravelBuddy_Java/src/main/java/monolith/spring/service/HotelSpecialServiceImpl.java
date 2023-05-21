package monolith.spring.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import monolith.spring.dao.HotelSpecialDAO;
import monolith.spring.model.HotelSpecial;

@Service
public class HotelSpecialServiceImpl implements HotelSpecialService {
	
	private HotelSpecialDAO hotelspecialDAO;

	
	private HotelSpecialDAO getHotelspecialDAO() {
		return hotelspecialDAO;
	}

	public void setHotelspecialDAO(HotelSpecialDAO hotelspecialDAO) {
		this.hotelspecialDAO = hotelspecialDAO;
	}

	@Override
	@Transactional
	public List<HotelSpecial> findAll() {
		return this.getHotelspecialDAO().findAll();
	}

	@Override
	@Transactional
	public HotelSpecial findById(int id) {
		return this.getHotelspecialDAO().findById(id);
	}

}
