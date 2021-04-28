import { Flex } from "@chakra-ui/react"

export const Layout = ({ children }) => {
    return (
    <Flex minH="100vH" width="full" align="center" justifyContent="center">
        {children}
    </Flex>
    )
};