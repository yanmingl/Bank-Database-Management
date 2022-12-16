# 1. Find the specific number of accounts that users whose first name is like "Ric"
use autobankms;
select u.firstName, count(*) as num_accounts
from users u, account a
where u.userID = a.accountID
and u.firstName like "%Ric%"
group by u.firstName;

# 2. Get the users' full name whose consulting employee belongs to sales department that sold product type is inveset.
select concat(u.firstName, ' ', u.lastName)
as user_whole_name, d.name as employee_department_name,
p.type as product_type
from users u, advised_by ab, employee e, department d, product p
where u.userID = ab.userID
and ab.employeeID = e.employeeID
and e.departmentID = d.departmentID
and d.departmentID = p.productID
and d.name = 'sales'
and p.type = "invest"
order by user_whole_name;

# 3. Get the money amount should be be paid by users(loan + credit cards)
set @loan_value =
(select (unitNum * unitPrice)
from purchase 
where productID in 
(select productID from product
where type = 'loan'));

set @credit_pay_back=
(select sum(cost - c.return) from creditcard c);

select @loan_value;
select @credit_pay_back;
select @loan_value + @credit_pay_back as all_money_payBack;

# 4. Get the profits that the bank earns for all products.
select pr.type, ((pu.unitPrice - n.unitCost) * pu.unitNum) as profits
from purchase pu, negotiate n, product pr, supplier s
where pu.productID = pr.productID
and pr.productID = s.productID	
and s.supplierID = n.supplierID
group by pu.productID

# 5. Get the manager's name and its level.	
# MySQL DO NOT SUPPORT THIS STATEMENT
with subManager(manageID, name, level) as 
(select managerID, name, 1
from manager where reporto = null)
union all
(select m.managerID, m.name, s.level+1
from subManager s, manager m where s.managerID = m.reporto);

select * from subManger order by level;

# 6. Get the average manageFeeMonth for the checkingacc
select avg(manageFeeMonth) from checkingacc;

# 7. Get all giftOrNot status of savingacc if the accountID do not belongs to checkingacc 
select * from savingacc;
select * from account;
create view checkingIDA as (select accountID, balance from account where accountID not in (select accountID from checkingacc));
create view checkingIDV as (select accountID, balance, if(balance>50000, "YES", "NO") as giftOrNot from checkingIDA);
select * from checkingIDV;
insert into savingacc(accountID, giftOrNot) select accountID, giftOrNot from checkingIDV;
select * from savingacc;
delete from savingacc;
