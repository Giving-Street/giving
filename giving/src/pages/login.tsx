import GoogleLogin from "react-google-login";
import styled from "@emotion/styled"
import {useCallback, useState} from "react";

const PageLayout = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
`

const Container = styled.div`
    min-height: 200px;
    display: flex;
    flex-direction: column;
`

const Box = styled.div`
    display: flex;
    flex-direction: column;
    max-width: 85vw;
    margin: 12px 0;
`

function GoogleLoginProvider() {
    const [token, setToken] = useState("")
    const handleLogin = useCallback(() => {
        console.log("login success")
    }, [])
    return (
        <Box className="google-provider">
            <GoogleLogin clientId={import.meta.env?.VITE_GOOGLE_CLIENT_ID as string} onSuccess={handleLogin}/>
        </Box>
    );
}

export const LoginPage = () => {
    return (
        <PageLayout className="login-page">
            Giving Street에 로그인 해주세요

            <Container className="login-providers">
                <GoogleLoginProvider/>
            </Container>
        </PageLayout>
    )
}