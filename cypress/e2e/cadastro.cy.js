describe('template spec', () => {
  it('passes', () => {
    cy.visit('http://127.0.0.1:8000/cadastro')

    cy.get("input[id='nome']").type("libertadores")
    cy.get("input[id='cpf']").type("999.999.999-99")
    cy.get("input[id='email']").type("example@gmail.com")
    cy.get("input[id='senha']").type("fJ&&#4445")
    cy.get("input[id='lembrar']").check()
    cy.get("button[id='cadastrar']").click()


  })
})