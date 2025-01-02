// import React from "react";
import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

import SearchDetailCards from "./SearchDetailCards";

import { useDispatch, useSelector } from "react-redux";

import { fetchTours, deleteTour } from "../redux/appReducer/myTourSlice";
const MyTours = () => {
  const dispatch = useDispatch();

  const { tours, status, error } = useSelector((state) => state.myTours);
  const [tourDays, setTourDays] = useState([]);
  const [tourName, setTourName] = useState([]);
  const location = useLocation();
  const data = location.state; //
  const arrayData = [
    {
      id: 1,
      title: "Pérez Art Museum Miami",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_1.png",
      price: "$50 - $200",
      stayTime: "3",
      city: "Miami",
    },
    {
      id: 1,
      title: "Hard Rock Stadium",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_2.png",
      price: "$50 - $80",
      stayTime: "1",
    },
    {
      id: 1,
      title: "Matheson Hammock Park",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_3.png",
      price: "$50 - $100",
      stayTime: "9",
    },
    {
      id: 1,
      title: "The Wharf Miami",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_4.png",
      price: "$50 - $200",
      stayTime: "2",
    },
    {
      id: 1,
      title: "Miami Tower",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_5.png",
      price: "$30 - $200",
      stayTime: "3",
    },
    {
      id: 1,
      title: "Skyviews Miami",
      description:
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente, eos. Rerum doloremque laboriosam ab ratione veritatis itaque dolor.",
      img: "/dest_test_img_6.png",
      price: "$50 - $200",
      stayTime: "7",
    },
  ];

  // Fetch tours when the component mounts
  useEffect(() => {
    const email = localStorage.getItem("useremail");
    if (status === "idle" && email) {
      dispatch(fetchTours());
    }
  }, [status, dispatch]);

  if (status === "loading") {
    return <p>Loading...</p>;
  }

  if (status === "failed") {
    return <p>Error: {error}</p>;
  }

  return (
    <div className="box">
      <h1 className="mt-5" style={{ color: "#202445" }}>
        My Tours
      </h1>

      {/* Modal for delete button */}

      {status === "loading" ? (
        <div class="spinner-container">
          <div class="spinner-border text-success" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      ) : error ? (
        <div>Error: {error}</div>
      ) : tours && tours.length > 0 ? (
        <div className="d-flex justify-content-center gap-5 pb-5 mt-4">
          <div className="wrapCards">
            {/* {arrayData &&
            arrayData.map(
              ({ title, description, img, price, stayTime, city }, index) => (
                <SearchDetailCards
                  key={index}
                  title={title}
                  description={description}
                  img={img}
                  price={price}
                  stayTime={stayTime}
                  city={city}
                  myTours={"myTours"}
                  setIsModalOpen={setIsModalOpen}
                  setTourDays={setTourDays}
                  setTourName={setTourName}
                />
              )
            )} */}

            {tours &&
              tours.map(
                (
                  {
                    tour_details,
                    _id,
                    user_name,
                    email,
                    phone_number,
                    adults,
                    children,
                    payment_method,
                  },
                  index
                ) => {
                  const { name, description, img, price, duration, city } =
                    tour_details;
                  console.log(" Here tour details are ", tour_details);
                  console.log(" city are ", city);
                  console.log(" Here Booking Id are ", _id);
                  console.log(" Here Booking user_name  ", user_name);
                  console.log(" Here Booking email  ", email);
                  console.log(" Here TourId  in My tour  ", tour_details._id);

                  return (
                    <SearchDetailCards
                      key={index}
                      title={name}
                      description={description}
                      img={img}
                      price={price}
                      stayTime={duration}
                      city={city}
                      bookingId={_id}
                      name={user_name}
                      email={email}
                      phone_number={phone_number}
                      adults={adults}
                      children={children}
                      payment_method={payment_method}
                      tourId={tour_details._id}
                      // refreshData={fetchData}
                      refreshData={() => dispatch(fetchTours())} //
                      myTours={"myTours"}
                      departureLocation={tour_details.departure_location}
                      returnDetails={tour_details.return_details}
                      // setIsModalOpen={setIsModalOpen}
                      setTourDays={setTourDays}
                      setTourName={setTourName}
                    />
                  );
                }
              )}
          </div>
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            height: "calc(100vh - 200px)",
          }}
        >
          <img
            src="/Search_Page_Img.svg"
            alt="Search"
            style={{
              maxWidth: "100%",
              maxHeight: "100%",
              objectFit: "contain",
              marginBottom: "1rem",
            }}
          />
          <p className="fs-2" style={{ textAlign: "center", color: "#797C9A" }}>
            Please add your tours
            <br />
          </p>
        </div>
      )}
    </div>
  );
};

export default MyTours;
