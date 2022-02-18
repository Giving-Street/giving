import styled from "@emotion/styled"
import {SERVER_URL} from "../constants";

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

export const LoginPage = () => {
    return (
        <PageLayout className="login-page">
            Giving Street에 로그인 해주세요

            <Container className="login-providers">
                <Box>
                    <a href={`${SERVER_URL}/auth/google/login`} >Login With Google</a>
                </Box>
            </Container>
        </PageLayout>
    )
}