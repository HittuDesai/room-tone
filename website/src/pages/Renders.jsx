import React from "react";
import colors from "@/constants/colors";
import { useRouter } from "next/router";
import rendering from "@/assets/rendering.png"
import rendering2 from "@/assets/rendering-2.png"
import upload from "@/assets/upload.png"
import upload2 from "@/assets/upload-2.png"
import rendered from "@/assets/rendered.png"
import rendered2 from "@/assets/rendered-2.png"

function OptionButton(props){
  const [onHover, setOnHover] = React.useState(false);

  return(
    <div
        style={onHover ? styles.hoverButtonContainer : styles.buttonContainer}
        onMouseEnter={() => {
          setOnHover(true);
        }}
        onMouseLeave={() => {
          setOnHover(false);
        }}
        onClick={()=>{props.clickButton()}}
      >
        <b>{props.title}</b>
    </div>
  )
}

function Renders() {
  const router = useRouter();
  
  return (
    <div style={styles.appContainer}>
      <div style={{display: 'flex', flexDirection: 'column'}}>
        <div style={{display: 'flex', flex: 1, flexDirection: 'row'}}>
          <OptionButton
            title="Bahen"
            src={upload}
            src2={upload2}
            clickButton={()=>{
                localStorage.setItem("RoomTone", "./poly.glb");
                router.push({
                    pathname: '/Show3D',
                });
            }}
          />
          <OptionButton
            title="GB"
            src={upload}
            src2={upload2}
            clickButton={()=>{
                localStorage.setItem("RoomTone", "./poly-1.glb");
                router.push({
                    pathname: '/Show3D',
                });
            }}
          />
        </div>
        {/* <>
          <OptionButton
            title="Pre-Loaded Renders"
            src={rendered}
            src2={rendered2}
            clickButton={()=>{router.push('/Show3D')}}
          />
        </> */}

      </div>
      
    </div>
  );
}

const styles = {
  appContainer: {
    display: "flex",
    justifyContent: "center",
    textAlign: "center",
    alignContent: "center",
    alignItems: "center",
    alignSelf: "center",
    backgroundColor: colors.cloudyWhite,
    height: "100vh",
    width: "100vw",
    flex: 1,
    flexDirection: "column",
  },
  buttonContainer: {
    backgroundColor: colors.lightMetallicBlue,
    width: "30vw",
    minHeight: "14vh",
    height: "auto",
    padding: 10,
    minWidth: "20vw",
    display: "flex",
    justifyContent: "center",
    textAlign: "center",
    alignContent: "center",
    alignItems: "center",
    alignSelf: "center",
    color: colors.midnightBlack,
    borderRadius: 20,
    cursor: "pointer",
    marginTop: "5vh",
    fontSize: 20,
    marginLeft: '5vw',
    marginRight: '5vw',
    flexDirection: 'column'
  },
  hoverButtonContainer: {
    backgroundColor: colors.midnightBlack,
    width: "30vw",
    minHeight: "14vh",
    height: "auto",
    padding: 10,
    minWidth: "20vw",
    display: "flex",
    justifyContent: "center",
    textAlign: "center",
    alignContent: "center",
    alignItems: "center",
    alignSelf: "center",
    color: colors.cloudyWhite,
    borderRadius: 20,
    cursor: "pointer",
    marginTop: "5vh",
    fontSize: 22,
    marginLeft: '5vw',
    marginRight: '5vw',
    flexDirection: 'column'
  },
};

export default Renders;